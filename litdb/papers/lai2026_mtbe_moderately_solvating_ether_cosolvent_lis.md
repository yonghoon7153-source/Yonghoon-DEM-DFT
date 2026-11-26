<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md (같은 절 구성)
     2026-11-26 신규 — 논문 에이전트 (inbox '7.' 본문 11 pp + SI 25 pp · 글자층 전문 정독 + 그림 크롭 실독).
     그림: tools/litdb/extract_figures.py --clean 1 회 → 손질 3 건 (figures.json 에 사유):
       ① 본문 6 장 다시 자름 (도구 판이 y≈72 pt 에서 시작해 패널 라벨 a) b) c) 와 윗부분이 잘렸다 · 위끝 58 pt 로)
       ② Fig. S4 · S8 손 크롭 (벡터 그림이라 도구가 '그래픽 없음' 으로 버림 · missing_labels 에 떴던 두 번호)
       ③ Fig. S9 손 크롭 (도구 판 fig_S9 가 같은 쪽 Fig. S10 래스터와 바이트 동일이었다)
     ⛔ 그림 폴더는 --clean 으로 다시 돌리지 않는다 — 위 손작업 4 장 (S4 · S8 · S9 + 본문 6 장 재크롭) 이 지워진다.
     ⚠ 이번 실행에서 도구가 litdb/figures/_sources.json 을 자동 갱신했다 — 이번 작업 범위 밖 (공유 색인 · 금지 목록) 이라 git checkout 으로 되돌렸다.
       이 논문은 _sources.json · pdf_map.tsv 에 아직 없다 (색인 갱신은 공유 표 담당 몫).
     talk 인입 대기열: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → lee2026_skku_mlip_materials_design.md 하나 · 이 논문 행 없음 (확인).
     ⚠ 이 논문은 **액체 (중간 용매화 · MSE) 전해질 Li–S 전지** 논문이다 — argyrodite SE 물성 4축 (A–D) 에 행을 만들지 않는다.
       쓰는 곳은 방법 (고전 MD 배위수 · AIMD 폴리설파이드 용매화 · 분자 DFT + 내재 용매 결합에너지) · 개념 (희석제형 용매화 조절 · β→α S₈) · 보고 규약 감사.
     우리 점착 W 값 · li2s 계열 값은 싣지 않는다 (위치만). 새 li2s 카드 · 트랙 · 런을 제안하지 않는다 (li2s 계열 2026-11-16 닫힘). -->

# Modulating Li⁺ and Polysulfide Solvation with Low-Density Moderately Solvating Electrolytes for Lithium–Sulfur Batteries — Lai, Liao & Manthiram (*Angew. Chem. Int. Ed.* 2026, 65, e22940)

> slug `lai2026_mtbe_moderately_solvating_ether_cosolvent_lis` · DOI `10.1002/anie.202522940` · type `mixed — exp 주 (Raman · ⁷Li/¹⁹F/¹H NMR · ¹H/⁷Li/¹⁹F DOSY · SAXS · Tafel/LSV · 온도별 EIS + DRT · Aurbach CE · GITT-EIS 분극 분해 · 정전위 Li₂S 석출 · Li₂S₆ 대칭셀 · operando/ex situ XRD · XPS 깊이 분석 · SEM · 코인/파우치) + 계산 보조 (GROMACS OPLS-AA 고전 MD 5 계 · VASP PBE AIMD 2 계 15 ps · Gaussian 16 B3LYP 최적화 + M06-2X-D3 단일점 + IEFPCM 결합에너지 · ESP) — NEB 0 · MLIP 0 · 슬랩 0 · DOS/Bader/COHP 0` · PDF `litdb/inbox/7. Modulating Li+ and Polysulfide Solvation with Low‐Density Moderately Solvating Electrolytes for Lithium–Sulfur Batteries.pdf` (본문 11 pp · Fig. 1–6 · sha256 `bbef90fa…628e249b`) + `litdb/inbox/7. Sup) Modulating …pdf` (SI 25 pp · Fig. S1–S29 · Table S1–S3 · 참고문헌 26 · sha256 `e0ea7c91…ab757d806`) · digested `2026-11-26` · status ✅ · 태그 **[외부 · 액체 전해질 Li–S (MSE) · 비-argyrodite]**
> elements: Li, S, O, C, N, F
> methods: DFT, AIMD, MD, XPS, Raman

> **저자**: **Tianxing Lai** · Kameron Liao · **Arumugam Manthiram\*** — The University of Texas at Austin (Materials Science and Engineering Program · Walker Department of Mechanical Engineering). 교신 rmanth@mail.utexas.edu.
> 접수 2025-10-19 · 수정 2025-11-30 · 수락 2025-12-28 · 온라인 2026-01-03 · *Angew. Chem. Int. Ed.* 2026, 65 (7), e22940 · 'Very Important Paper' 표지 · 오픈액세스 (CC BY-NC-ND). 자금: U.S. DOE BES DE-SC0005397 · Bard Center 장학 (T. Lai, Welch Foundation H-F-0037). 계산 자원 TACC. 감사: Dr. Biyu Jin (DFT 계산 도움) · Dr. Hugo Celio (XPS). 이해 상충 없음 · 데이터는 '요청 시'.
> 기여 진술: **없다** (Angew 양식에 CRediT 절이 없다) — DFT 는 감사 문구로 보아 Biyu Jin 이 도왔다. 부속 파일: inbox 에 이 논문 번호 ('7.') 의 xlsx · zip · 영상은 **없다** (확인).
> **계보**: Manthiram 그룹 Li–S 전해질 계열 — Lai 2023 *Adv. Funct. Mater.* (ref 13) · Lai 2024 *Adv. Funct. Mater.* (ether 전해질 β-S₈ · ref 44) · Jin 2023 *ACS Energy Lett.* (XPS S 2p 귀속 · ref 46) · Liao 2025 *Adv. Energy Mater.* (분무건조 KB 숙주 · ref 43 · SI ref 1) → **본 논문**. 같은 'MSE' 개념의 앞선 판: Kautz 2025 *Adv. Mater.* (ref 32) · Kim 2025 *Adv. Energy Mater.* (불소 공용매 MSE · ref 33) · Gao 2023 *PNAS* (중간 LiPS 용해도 · ref 34). 대조로 인용된 SSE 계: Liu 2025 *Nat. Chem.* (Pang · BDTS–LiTFSI–CPME · ref 24) · Liu 2023 *Joule* (반용매 준고체 · ref 27).
> 🔗 **이어 읽기 (litdb)**: 같은 CPME 를 다른 자리에 쓴 `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` (거의 짝 논문 — §14) · 준고체 Li–S `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` · `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` · 액체 Li–S `guan2026_feco_vs_in2s3_li2s_electrocrystallization` · `wei2026_data_driven_hea_mediator_lis` · 전고체 Li–S `yu2025_cng_host_suppress_argyrodite_oxidation_lis` · `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` · `cronk2026_lis_cathode_interphase_chemistry` — 대응은 §14.

---

## 0. 이 digest 를 읽는 법

**읽기축 (우리 트랙에서의 자리)**: 황화물 SE 가 아니라 **액체 전해질** (1 M LiTFSI + 0.2 M LiNO₃ · DOL/DME 에 단일 산소 에테르 30 vol%) Li–S 전지다. 가져올 것은 셋이다 — ① **계산 방법 대조** (고전 MD 배위수 · VASP AIMD Li₂S₆ 용매화 · 분자 DFT + IEFPCM 결합에너지 ↔ 우리 UMA MLIP-MD · ORCA r2SCAN-3c), ② **개념** (약용매화 '희석제' 가 Li⁺ 껍질에서 강용매 (DME) 를 빼내 접촉 이온쌍 · LiF 풍부 SEI 를 만드는 꼴 — 국소 고농도 (LHCE) 전해질과 같은 계열의 논리 · 재충전 S₈ 다형 β → α), ③ **보고 규약 반례** (본문 수치 ↔ 자기 그림이 어긋나는 자리 · 결정적 대조군 부재 — §10).

**판정 요약 (§6 · §10 상세)**:

| 주장 | 판정 | 핵심 근거 |
|---|---|---|
| 단일 산소 에테르 (MtBE 등) 30 vol% 가 Li⁺–DME 배위를 약하게 하고 양이온–음이온 회합을 늘린다 | ✅ 방향은 받친다 | 고전 MD CN(O_DME) figure-read ≈3.6 → ≈3.0 (`Fig. 2d`) · Raman 띠 741.6 → 742.5–743.1 cm⁻¹ · ⁷Li 저자장 이동 |
| MSE 가 LiPS **용해를 제한**한다 | 🔴 정량 근거 없음 | 용해도 측정값이 논문에 **하나도 없다** · `Fig. 1c` · `Fig. S2` 사진은 MtBE 를 **더 부어** 희석한 것이라 색 변화가 희석과 섞인다 · 1:1 에서도 침전이 안 보인다 (§5.4) |
| 탈용매화 장벽을 낮춘다 (초록) | ⚠ MtBE 만 · 차이 1 % | Li\|Li Rct Ea 64.3 (기준) 대 63.6 (MtBE) · **CPME 67.3 · SBME 66.5 · TAME 66.0 kJ mol⁻¹ 은 기준보다 높다** (`Fig. 2f`) · 저자도 '비슷하다' 라 씀 |
| Li 금속 쪽 안정화 (CE 98.0 → 99.5 % · 600 h 대칭셀) | ✅ 받친다 (셀 각 1) | `Fig. 2g,h` · i₀ ≈0.19 → ≈0.43 mA cm⁻² (`Fig. S9`, figure-read) · XPS Li–F/C–F↑ |
| 셔틀 억제 | ✅ 방향 · ⚠ 크기 | 2.25 V 유지 전류 0.047 → 0.013 mA (`Fig. S15`) · 45 °C CE ≈94–95 % (기준 ≈91 → ≈84 %) — 94.6 % 도 사이클당 ≈5 % 손실이다 |
| 충전 끝 β-S₈ → α-S₈ 의 '두 단계 S 석출' 이 MSE 의 특징이다 | ⚠ 관찰 ✅ · 해석 🔴 | operando XRD 에 실제로 보인다 (`Fig. 4a`) · 그러나 β-S₈ 는 실온 준안정이라 시간만 지나도 α 로 간다 — ex situ 담금 실험 (`Fig. S23`) 에 DOL/DME 담금 · 시간 대조가 없다 |
| 고율 (C/2) 781 mAh g⁻¹ | 🔴 그림과 다르다 | `Fig. 5b` C/2 구간 figure-read ≈690–712 · `Fig. 5c` C/2 방전 ≈720 — 781 은 C/0.4 (0.4C) 구간 값에 가깝다 (§10-⑦) |
| 45 °C · 3.6 mg cm⁻² 90 사이클 799 mAh g⁻¹ · 첫 CE 79.7 % | ✅ 용량 · ⚠ CE | `Fig. 5d` 용량은 맞다 · `Fig. 5e` 첫 사이클 곡선은 방전 ≈1280 / 충전 ≈1430 (figure-read) 로 ≈89 % 라 79.7 % 와 안 맞는다 (CE 정의 미기재) |
| 파우치 (3.5 mg cm⁻² · 5.5 µL mg⁻¹ · 70 cyc 768 mAh g⁻¹) | ⚠ 규모 작음 | 양극 한 장 5.6 × 4.3 cm (≈24 cm²) · Ah · Wh kg⁻¹ 미보고 → 우리 산수로 ≈65 mAh 급 (§3d) |

**본 digest 에서 실제로 본 그림 (2026-11-26)** — 크롭 PNG 38 장 (본문 Fig. 6 + SI Fig. 29 + 표 3) 중:

- 원해상도로 본 것 **23 장**: `Fig. 1`–`Fig. 6` (본문 6 · 다시 자른 판) · `Fig. S2` · `S3` · `S4` · `S7` · `S8` · `S9` · `S10` · `S12` · `S13` · `S14` · `S15` · `S16` · `S18` · `S21` · `S23` · `S24` · `S27` (SI 17).
- 확대해서 다시 읽은 패널: `Fig. 5b` · `Fig. 5e` (600 dpi 렌더).
- 축소 접촉 시트로 본 것 **12 장**: `Fig. S1` · `S5` · `S6` · `S11` · `S17` · `S19` · `S20` · `S22` · `S25` · `S26` · `S28` · `S29` (인쇄 숫자 · 곡선 모양 · 축 라벨 확인 수준).
- **안 본 것**: `Table S1` · `Table S2` · `Table S3` (표는 PDF 글자층으로 읽었다).
- 그림에서만 읽은 값은 **`figure-read ≈`** 로 적었다. 픽셀 판독 정밀도는 눈금 간격의 ≈ ±2–5 % 다.

---

## 1. 한 줄 요약

표준 Li–S 전해질 (1 M LiTFSI + 0.2 M LiNO₃ in DOL/DME 1:1) 의 용매 30 vol% 를 밀도 · 점도가 낮은 비불소 단일 산소 에테르 넷 (MtBE · CPME · SBME · TAME) 중 하나로 바꾼 '중간 용매화 전해질 (MSE)' 을 만들고, 그중 **MSE-MtBE** 가 Li⁺–DME 배위를 가장 많이 덜어 내 (고전 MD CN ≈3.6 → ≈3.0) 접촉 이온쌍 · LiF 풍부 SEI · Li CE 99.5 % · 셔틀 전류 ≈1/3.6 · 45 °C 사이클 안정성을 준다고 보고한다. 저자 해석은 "용매–용매 · 용매–음이온 상호작용으로 Li⁺ 와 폴리설파이드의 용매화를 **동시에** 조절한다" 이다. Li 음극 쪽 결과는 데이터가 대체로 받치지만, '폴리설파이드 용해 제한' 은 **측정값이 없고**, '탈용매화 장벽 감소' 는 MtBE 에서만 0.7 kJ mol⁻¹ 이며, 이 효과가 MtBE 의 고유 화학인지 **'희석으로 염/강용매 비가 1.43 배 오른 효과'** 인지 가르는 대조군이 없다.

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | 기준: 1 M LiTFSI + 0.2 M LiNO₃ in DOL/DME (1:1 v/v) · MSE: 같은 염 in DOL/DME/X (3.5:3.5:3 v/v/v), X = MtBE · CPME · SBME · TAME. 대칭셀용 0.1 M Li₂S₆ 첨가 |
| 양극 | 분무건조 KB (EC-600JD) + S 75 wt% · 155 °C 12 h 용융 확산 · 45 µm 체 → S/KB 85 + CNT 5 + C65 5 + PAA 4 + Na-CMC 1 (수계) · 탄소 코팅 Al · 지름 7/16 in. 파우치 (≥ 4.5 mg cm⁻²) 는 S 70 wt% 복합체 + C65 5 + Na-CMC 4 |
| 음극 | Li 금속 (파우치는 Ni 집전체에 압착) |
| 질문 | DOL/DME 는 동역학은 괜찮지만 셔틀을 못 막고, LHCE · WSE (약용매화) 는 셔틀 · Li 안정성은 좋지만 이온 이동 · 점도 · 동역학이 나쁘며 불소 희석제가 비싸고 무겁다. **중간 (moderate) 지점을 어떤 공용매로 잡나 — 그리고 그 공용매가 Li⁺ · 폴리설파이드 용매화를 실제로 어떻게 바꾸나?** (저자: "co-solvent 고르는 기준과 LiPS 용매화 이해가 부족하다") |
| 후보 선택 논리 | O 원자 하나 + 입체 장애 → Li⁺ 용매화 약함 · 비용매 (불소 에테르) 와 달리 **약간은 용매화** · LiPS 용해도는 DME/DOL 보다 훨씬 낮다 (근거: 사진 `Fig. 1c` · `Fig. S2`) · 저밀도 (MtBE 0.741 g cm⁻³ · `Table S1`) |
| 답 (저자) | MSE-MtBE 가 ① Li⁺–용매 결합을 약하게 하고 양이온–음이온 회합을 강하게 하며 ② 폴리설파이드 용해를 줄이면서 젖음성 · 물질 이동을 개선 → Li⁺ 탈용매화 쉬움 · LiF 풍부 부동태 SEI · 바뀐 S 석출 경로 (β → α) (`Fig. 1a` 모식도) |
| 연구 유형 | 실험 주 · 계산 보조 (계산은 해석 받침 그림 여섯: `Fig. 1d,e` · `Fig. 2d,e` · `Fig. 3d–f` · `Fig. S1` · `Fig. S6` · `Fig. S7` · `Fig. S14`) |
| 우리와의 거리 | 황화물 SE 물성 4축 (A 이온 · B 산화 · C 기계 · D 전자) 수치 비교 없음. 방법 · 개념 · 보고 규약 쪽만 닿는다 (§7) |

## 3. 핵심 수치 총정리 ★

> 규율: 아래는 전부 **문헌 소환값**이다 — 우리 db 절대값과 한 표에 섞지 않는다. 본문 명시값과 `figure-read ≈` 를 칸마다 구분했다.
> 온도는 따로 적지 않으면 21 °C (논문의 '실온').

### 3a. 전해질 물성 · 용매화 (분광)

| 물성 | DOL/DME | MSE-MtBE | 다른 MSE | 출처 · 비고 |
|---|---|---|---|---|
| 밀도 (g cm⁻³) | **1.16** | **1.04** | n/a | 본문 (측정법 미기재) |
| 이온전도도 σ (mS cm⁻¹) | **11.68** | **7.11** | n/a | `Fig. S21` (전도도 측정기 · 탐침 · 실온) — MSE 가 **−39 %** |
| 용매 상수 (`Table S1` · 판매사 · 문헌) | DME 0.869 / 0.46 cP / ε 7.2 · DOL 1.06 / 0.6 / 7.3 | MtBE 0.741 / 0.27 / 4.5 | CPME 0.86 / 0.55 / 4.76 · SBME 0.742 / n/a / n/a · TAME 0.77 / 0.51 / n/a | SBME 점도는 없어 `Fig. 1b` 에 0.4 를 임의로 넣었다 (표 주석) |
| Raman S–N–S 띠 중심 (cm⁻¹) | **741.6** | 742.5–743.1 (MSE 넷 범위) | 같은 범위 | `Fig. S3` · 두 성분 맞춤 (≈740 자유/SSIP · ≈745 CIP/AGG) — CIP 와 AGG 를 따로 가르지 않았다 · 맞춤 분율 숫자 없음 |
| ⁷Li NMR (ppm, 1 M LiTFSI 전해질) | **−1.19** | figure-read ≈ −1.11 | SBME ≈ −1.10 · TAME ≈ −1.125 · CPME ≈ −1.17 | `Fig. 2a` · LiPF₆ 동축 기준 ≈ −1.06 · 저자장 이동 크기 SBME ≳ MtBE > TAME > CPME |
| ¹⁹F NMR TFSI⁻ (ppm) | **−80.17** | figure-read ≈ −80.21 | TAME ≈ −80.27 · SBME ≈ −80.27 · CPME ≈ −80.31 (봉우리 갈라짐) | `Fig. S4` (손 크롭) · MtBE 의 고자장 이동이 가장 작다 |
| ¹⁹F DOSY D(TFSI⁻) (m² s⁻¹) | **5.01 × 10⁻¹⁰** | **4.37 × 10⁻¹⁰** | n/a | 본문 · `Fig. S5` (log D ≈ −9.30 · −9.36) |
| Li⁺–용매 결합에너지 (eV, DFT) | DME **0.643** · DOL figure-read ≈0.275 | figure-read ≈0.15 | CPME **≈0.325** · SBME ≈0.13 · TAME ≈0.15 | `Fig. 1d` · 본문 "three of the four … ∼0.15 eV" |
| Li⁺–O 거리 (Å, DFT 최적 구조) | DME 1.998 / 1.990 · DOL 1.946 | **2.555** | CPME 1.921 · SBME 2.570 · TAME 2.560 | `Fig. 1e` — MtBE · SBME · TAME 는 **2.55 Å 넘게 떨어져** 있다 (§10-③) |
| DME–용매 결합에너지 (eV, DFT) | DOL figure-read ≈0.168 | **0.189** | CPME ≈0.174 · SBME ≈0.185 · TAME ≈0.182 | `Fig. 2e` · 최대–최소 0.021 eV |
| SAXS 주 봉우리 | q figure-read ≈1.47 Å⁻¹ (d ≈4.3 Å) | q ≈1.40 Å⁻¹ (d ≈4.5 Å) | — | `Fig. S8` (손 크롭) · 저 q (< 0.1 Å⁻¹) 세기 ≈0.012 대 ≈0.030 (임의 단위 · figure-read) |

### 3b. 계산 (전부 문헌 소환값 · 방법은 §4e · §8)

| 양 | 값 | 출처 | 비고 |
|---|---|---|---|
| 고전 MD 상자 조성 | `Table S3` — DOL/DME 736 DOL · 495 DME · 103 LiTFSI · 21 LiNO₃ / MSE-MtBE 544 · 366 · 274 MtBE · 109 · 22 / MSE-CPME 528 · 355 · 272 CPME · 105 · 21 / MSE-SBME 544 · 366 · 274 · 109 · 22 / MSE-TAME 540 · 363 · '244 MtBE' · 108 · 22 | `Table S3` | **우리 검산**: 부피비 3.5:3.5:3 · [LiTFSI] 1.00 M · [LiNO₃] 0.20 M 이 다섯 계 모두 맞는다 (밀도 `Table S1`). TAME 행의 '244 MtBE' 는 TAME (102.17 g mol⁻¹ · 0.77) 로 셀 때만 53.8 nm³ (≈3 몫) 가 맞아 **TAME 의 오기**다 |
| CN(O_DME) — 첫 껍질 평탄 | DOL/DME figure-read ≈3.6 · CPME ≈3.25 · TAME ≈3.15 · SBME ≈3.08 · MtBE ≈3.03 | `Fig. 2d` | ⚠ 이 그림만 색이 다르다 (SBME 파랑 · TAME 초록 · CPME 주황 — 다른 그림은 CPME 파랑 · SBME 초록 · TAME 보라). 범례 기준으로 읽었다 |
| CN(O_X) — 공용매 산소 | SBME ≈0.20 · MtBE ≈0.18 · CPME ≈0.09 · TAME ≈0.085 | `Fig. S7` | Li–O 봉우리 ≈1.87 Å · g(r) 봉우리 SBME ≈16.5 · MtBE ≈15 · TAME ≈8.3 · CPME ≈7.5 — ⚠ DFT 로는 CPME 가 Li⁺ 와 **가장 세게** 붙는데 (0.325 eV) MD 로는 첫 껍질에 **가장 적게** 들어간다 (§10-④) |
| AIMD 상자 | MSE-MtBE: 15 DOL · 10 DME · 7 MtBE · 3 LiTFSI · 1 LiNO₃ · 1 Li₂S₆ in 1.8³ nm³ / DOL/DME: 20 DOL · 14 DME · 3 LiTFSI · 1 LiNO₃ · 1 Li₂S₆ in 1.75³ nm³ | SI Computational | **우리 산수**: 원자 512 / 505 · 밀도 ≈1.07 / ≈1.20 g cm⁻³ · [LiTFSI] ≈0.85 / ≈0.93 M · [Li₂S₆] ≈0.28 / ≈0.31 M (실험 대칭셀 0.1 M 의 ≈3 배) · Li⁺ 총 6 개 · S₆²⁻ 1 개 |
| S(S₆²⁻)–Li⁺ g(r) | 첫 봉우리 r figure-read ≈2.5 Å · 높이 MSE-MtBE ≈22 · DOL/DME ≈15 · 둘째 ≈3.6 Å 에서 ≈7 대 ≈4 | `Fig. 3f` | **S₆²⁻ 1 개 · 5 ps 평균 · 궤적 1** · CN 숫자 미보고 |

### 3c. 전기화학 · 동역학

| 측정 | DOL/DME | MSE-MtBE | 다른 MSE · 비고 |
|---|---|---|---|
| Li\|Li 교환전류 i₀ (Tafel, mA cm⁻²) | figure-read ≈0.19 | ≈0.425 | CPME ≈0.378 · SBME ≈0.40 · TAME ≈0.382 (`Fig. S9` · 손 크롭) — ±100 mV 곡선에 뚜렷한 직선 구간이 없다 |
| Li\|Li Rct 겉보기 Ea (kJ mol⁻¹, 0–50 °C · DRT) | **64.3** | **63.6** | CPME **67.3** · SBME **66.5** · TAME **66.0** (`Fig. 2f`) — 점 6 개 · 셀 1 · 오차 미보고 |
| Li\|Li 0 °C Nyquist 반원 폭 (Ω) | figure-read ≈760 | ≈450 | CPME ≈600 · SBME ≈680 · TAME ≈590 (`Fig. S10`) |
| Li\|Li DRT 주 봉우리 τ (0 °C) | ≈3 × 10⁻³ s (γ ≈385 Ω) | ≈2 × 10⁻³ s (γ ≈240 Ω) | `Fig. S11` (접촉 시트 판독) |
| Aurbach CE (Li\|Ni · 0.5 mA cm⁻²) | **98.0 %** | **99.5 %** | CPME **99.4** · SBME **98.7** · TAME **98.9 %** (`Fig. 2g` · `Fig. S12`) — 그림 라벨 '0.5 mA cm⁻¹' 은 단위 오기 |
| Li\|Li 대칭 (1 mA cm⁻² · 1 mAh cm⁻²) | figure-read ≈300 h 부터 분극 증가 · ≈400 h 부터 진동 · ≈540 h 에 그림에서 끝남 (본문 "failed after 400 h") | 600 h 까지 ±≈0.04 V (끝에서 ≈0.05 로 넓어짐) | `Fig. 2h` |
| 0.1 M Li₂S₆ 용액 ⁷Li (ppm) | **0.17** | **0.28** | SBME ≈0.26 · TAME ≈0.23 · **CPME ≈0.15 (유일하게 고자장)** (`Fig. 3a`) |
| ¹H DOSY D(DME) · ⁷Li DOSY D(Li⁺) in Li₂S₆ 용액 (m² s⁻¹) | 1.26 × 10⁻⁹ · 4.47 × 10⁻¹⁰ | 1.91 × 10⁻⁹ · 5.62 × 10⁻¹⁰ | 본문 · `Fig. 3b,c` (log D −8.90/−8.72 · −9.35/−9.25 확인) — ⚠ `Fig. 3c` 의 ⁷Li 화학 이동 (≈0.0 · ≈0.24 ppm) 은 `Fig. 3a` (0.17 · 0.28) 와 다르다 |
| 셔틀 전류 (2.25 V 유지 · 3.5 mg cm⁻² · E/S 10) | **0.047 mA** (≈0.07 mA 정점 뒤 감소) | **0.013 mA** (−0.1 mA 에서 시작 · ≈1 h 에 0 을 지나 ≈0.018 → 0.013) | `Fig. S15` · **우리 산수**: 원판 0.970 cm² × 3.5 mg = 3.4 mg S → ≈13.9 · ≈3.8 mA g⁻¹ (≈C/108 · ≈C/390, 1C = 1500 mA g⁻¹) |
| GITT-EIS 분극 (C/10 · 15 min / 75 min · 3.5 mg cm⁻²) | η_ohm 정점 **2.10 mV** · η_act 정점 **10.4 mV** · η_conc ≈25 % DOD **47.4 mV** | η_ohm **2.81** · η_act **19.5** · η_conc **44.7 mV** | `Fig. 3g` · `Fig. S16` · 끝 구간 η_conc figure-read: 84 % ≈75 대 ≈47 · 88 % ≈203 대 ≈55 · 92 % ≈305 대 ≈158 · 96 % ≈390 대 ≈358 · 100 % 둘 다 ≈435 mV |
| 정전위 Li₂S 석출 (Li₂S₈ · 2.08 V) | 정점 figure-read ≈0.70 mA · t_m **0.266 h** · **161 mAh g⁻¹** | 정점 ≈1.06 mA · t_m **0.234 h** · **232 mAh g⁻¹** | `Fig. S18` · Li₂S₈ 농도 · 양 · 전극 · 배경 처리 미기재 |
| Li₂S₆ 대칭셀 Rct Ea (kJ mol⁻¹) | **44.4** | **41.1** | `Fig. 3i` · ln Rct figure-read 50 °C −0.37 대 0.40 · 0 °C 2.65 대 3.20 → Rct 는 MSE 가 **1.7–2.2 배 높다** (§5.6) |
| Li₂S₆ 대칭셀 0 °C 반원 (Ω) | figure-read ≈17 (R_s ≈2.5) | ≈32 (R_s ≈5) | `Fig. S19` |

### 3d. 셀 성능

| 조건 | DOL/DME | MSE-MtBE | 출처 · 비고 |
|---|---|---|---|
| 2.2 mg cm⁻² · E/S 18 · C/3 · 200 cyc | 537 mAh g⁻¹ · **59.3 %** | 첫 945 → 711 · **75.2 %** | 본문 · `Fig. S24` — E/S 18 은 그림에만 있다 · 기준은 ≈62 cyc 에 작은 계단 상승 |
| 3.7 mg cm⁻² · E/S 10 · C/5 · 180 cyc | 458 · **56.6 %** (함의 첫값 ≈809) | 894 → **710 · 79.4 %** | `Fig. 5a` · `Table S2` (첫 894) · 화성 (회색 띠) 뒤 첫 C/5 를 '처음' 으로 잡았다 |
| 3.6 mg cm⁻² · C/10 · 140 cyc | n/a | 1,019 → **848 · 83.2 %** | `Fig. S25` (화성 ≈1410 · ≈1180 figure-read) |
| 율 (3.5 mg cm⁻² · E/S 10) | figure-read 0.1C ≈940→850 · 0.2C ≈790–760 · 0.3C ≈735–720 · 0.4C ≈700–650 · **0.5C ≈630 → 545** · 복귀 0.2C ≈700 → ≈680 | 0.1C ≈1010→930 · 0.2C ≈870–840 · 0.3C ≈820 · 0.4C ≈780–760 · **0.5C ≈712 → ≈690** · 복귀 0.2C ≈855 → ≈820 | `Fig. 5b` (600 dpi 확대) — 본문 'C/2 에서 781 대 700' (§10-⑦) · 기준 셀은 복귀 구간 ≈58–59 cyc 에 **용량 0 점 두 개** (미언급) |
| 율별 방전 곡선 용량 | figure-read 0.1C ≈915 · 0.2C ≈790 · 0.3C ≈750 · 0.4C ≈695 · 0.5C ≈625 | 0.1C ≈995 · 0.2C ≈860 · 0.3C ≈815 · 0.4C ≈795 · 0.5C ≈720 | `Fig. S26` · `Fig. 5c` · MSE 0.5C 는 둘째 평탄 시작에서 ≈1.82 V 로 깊게 패인다 (본문 "larger dip") |
| 45 °C · 3.6 mg cm⁻² · E/S 10 · C/5 · 90 cyc | 첫 C/5 **770** → **627** · 평균 CE **89.4 %** · 화성 첫 CE **38.5 %** | 799 (90 cyc) · 평균 CE **94.6 %** · 화성 첫 CE **79.7 %** | 본문 · `Fig. 5d,e` · `Fig. S27` — CE figure-read: 기준 ≈91.5 → ≈83.5 % (≈35 cyc 부터 하락) · MSE ≈94–95.5 % · 다른 MSE ≈93 → ≈88–90 % (CPME 최저 · 흩어짐 큼) |
| 45 °C 첫 사이클 곡선 | 방전 figure-read ≈1165 · 충전은 ≈2.30 V 평탄으로 1600 넘게 이어지며 2.8 V 에 못 닿음 | 방전 ≈1280 · 충전 ≈1430 에서 2.8 V | `Fig. 5e` (600 dpi 확대) |
| 파우치 3.5 mg cm⁻² · E/S 5.5 · C/10 · 70 cyc | n/a | 768 mAh g⁻¹ (70 cyc) · figure-read 화성 ≈1230 · ≈1110 · ≈1045 → C/10 ≈800 → ≈850 (40 cyc) → ≈770 | `Fig. 5f` |
| 파우치 4.6 mg cm⁻² · E/S 4.5 · C/20 · 20 cyc | n/a | 779 (20 cyc) · `Table S2` 첫 773 · figure-read 첫 (C/30) ≈1090 | `Fig. S28` |
| 파우치 규모 (**우리 산수** · 한 면 가정) | — | 양극 5.6 × 4.3 cm ≈24 cm² × 3.5 mg = ≈84 mg S → 768 mAh g⁻¹ 에서 ≈65 mAh · 전해액 ≈0.46 mL | SI Pouch 절 — 양극 장수 · 양면 여부 · Ah · Wh kg⁻¹ 미기재 |

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 전해질
- Ar 글로브박스 · 분자체 건조 (기간 · 수분 함량 미기재). LiTFSI (Solvionic) · LiNO₃ (Sigma) · DOL (Thermo) · DME (Oakwood) · MtBE · CPME (Thermo) · SBME · TAME (Sigma).
- 기준 1 M LiTFSI + 0.2 M LiNO₃ in DOL/DME (1:1 v/v) · MSE 같은 염 in DOL/DME/X (3.5:3.5:3 v/v/v).
- **우리 산수 (희석 효과의 크기)**: MSE 는 강용매 (DOL+DME) 가 부피의 70 % 인데 염은 1 M 그대로다 → 강용매 부피 기준 염 농도 1.43 배. 몰로는 DOL:DME:MtBE ≈ 0.0501 : 0.0338 : 0.0252 mol mL⁻¹ (몰분율 MtBE ≈23 %). LHCE 와 같은 '강용매 대비 염 비↑' 효과가 이 설계에 **자동으로 들어간다** (§10-①).

### 4b. 전극 · 셀
- 코인 CR2032 · Celgard 2325 한 장 · 대칭셀 양쪽 20 µL · 5 h 휴지.
- 저하중 (~2 mg cm⁻²): C/20 한 번 + C/10 한 번 활성화. 고하중 (≥ 3.5): C/30 방전 → C/20 화성 1 회 (C/5 시험은 C/10 화성 추가). 1.7–2.8 V · 21 °C. 45 °C 는 C/20 두 번 + C/10 두 번 화성. Landt · Arbin.
- 1C = 1500 mA g⁻¹ (본문) — 이론 1672 가 아니다.
- 파우치: Li 박을 Ni 집전체에 압착 · 양극 5.6 × 4.3 cm (≈24 cm²) · 음극 5.8 × 4.5 cm · Ni/Al 탭 · 압력 홀더 (압력 값 미기재) · 3.5 mg cm⁻² 는 C/20 화성 2 회 후 C/10 · 4.6 mg cm⁻² 는 C/30 1 회 후 C/20.

### 4c. 전기화학
- **GITT-EIS**: C/10 · 15 min 방전 + 75 min 휴지 · 휴지 시작 3 min 뒤 EIS. η_ohm = 고주파 절편 × 전류 · η_ohm + η_act = 전류 계단의 순간 전압 점프 · η_conc = 휴지 중 평형으로의 느린 표류 (본문 정의). 분해 식 · R 를 η 로 바꾼 곱셈 · EIS 맞춤 미기재.
- **CV**: Li\|S 1.7–2.8 V · Li₂S₆ 대칭 −1 ~ 1 V (5 mV s⁻¹ · 5 사이클 · `Fig. S22`).
- **EIS**: 1 MHz – 0.05 Hz · DRT = pyDRTtools (정규화 매개변수 · 기저 함수 미기재). Rct = DRT 봉우리 면적 (`Fig. S11` 캡션). Biologic VMP-3.
- **Tafel**: Li\|Li LSV → Tafel 맞춤 → i₀ (주사 속도 · 맞춤 구간 미기재).
- **Aurbach CE**: Li\|Ni · 0.5 mA cm⁻² (프로토콜은 그림에서: 0–10 h 증착 → ≈19.5 h 까지 박리 · 20–30 h 증착 · 30–50 h 짧은 사이클 10 회 · 50 h → 박리 끝. 계산식 미기재).
- **셔틀 전류**: Li\|S 방전 중 2.25 V 에서 10 h 유지.
- **정전위 Li₂S 석출** (`Fig. S18`): "Li₂S₈ discharged at 2.08 V" — 촉매액 농도 · 부피 · 전극 · 사전 방전 · 배경 빼기 **전부 미기재** (Methods 에 절이 없다).
- **operando XRD**: Rigaku Ultima IV · MTI 특수 셀 · **C/25** (그림에만) · 주사 조건 미기재.
- **ex situ XRD** (`Fig. S23`): DOL/DME 1 사이클 뒤 양극을 MSE-MtBE 에 담금 — 담금 시간 · 온도 · 세척 · 대조 담금 미기재.

### 4d. 분석
- **NMR**: Bruker Avance III 500 MHz 또는 Agilent MR400 · DOSY = Varian 600 MHz · 동축 기준 0.1 M LiPF₆ in DMSO-d₆. 어느 그림이 어느 기기인지 미기재 (§10-⑨).
- **SAXS**: Xenocs Ganesha (절대 세기 보정 · 모세관 · 배경 빼기 미기재).
- **Raman**: Renishaw (파장 · 분해능 미기재) — 그림 y 축 라벨은 'Absorbance' (§10-⑪).
- **σ**: Mettler-Toledo SevenCompact S230 + InLab 752 탐침 (온도 보정 미기재).
- **SEM**: Apreo 2C LoVac. **XPS**: PHI VersaProbe 4 · Ar 클러스터 이온 스퍼터 (에너지 · 클러스터 크기 · 속도 미기재). 시료 세척 · 공기 차단 이송 **미기재**.
- **젖음** (`Fig. S17`): 양극 위 방울 0 · 25 ms 사진 한 쌍 (접촉각 · 방울 부피 미기재).

### 4e. 계산 (전부) ★

| 계산 | 적힌 것 | 안 적힌 것 |
|---|---|---|
| **분자 DFT** (`Fig. 1d,e` · `Fig. 2e` · `Fig. S1`) | Gaussian 16 · 최적화 B3LYP-D3(BJ)/6-311+G(d,p) · 진동 계산으로 극소 확인 · 단일점 M06-2X-D3/ma-def2-TZVP(-f) · IEFPCM 용매 효과 · ESP = Multiwfn + VMD 1.9.3 · 식 `E_binding = E_total − E_solvent − E_remain` | IEFPCM 의 **용매 (유전율)** · 최적화도 PCM 안에서 했는지 · 부호 규약 (식대로면 결합이 음수인데 그림은 양수) · BSSE (counterpoise) · 배좌 탐색 · ΔG 아님 (전자 에너지) · Li⁺ 1 개 + 리간드 1 개라는 **착물 정의의 선택** |
| **고전 MD** (`Fig. 2d` · `Fig. S6` · `Fig. S7`) | GROMACS 2024 · OPLS-AA · AuToFF 매개변수 · 용매 1.2*CM5 전하 · TFSI⁻ · NO₃⁻ 0.8*OPLS-2009IL (전하 0.8 배) · Packmol 6.5³ nm³ · CG 최소화 → 298 K 1 ns 가열 → NPT 1 bar 15 ns · 마지막 5 ns 통계 · 1 fs · C-rescale · V-rescale · 분자 수 `Table S3` | 시드 수 (하나로 보인다) · 컷오프 · PME · Li⁺ 매개변수 출처 · 전하 0.8 배 (이온) 와 1.2 배 (용매) 의 혼합이 어떤 실험값에 맞춰졌는지 · 평형 판정 (밀도 수렴) · CN 적분 반경 · 잔류 시간 |
| **AIMD** (`Fig. 3d–f` · `Fig. S14`) | VASP 6.4.2 · PAW · PBE · ENCUT 550 eV · Γ 점만 · Packmol · 분자 수 (§3b) · 1.8³ / 1.75³ nm³ · 300 K NVT Nosé–Hoover · **15 ps** · 마지막 5 ps 통계 · 1 fs · H → 삼중수소 질량 · VESTA 그림 | **분산 보정 (AIMD 에 D3 가 안 적혀 있다)** · 초기 Li₂S₆ 배치 (Li⁺ 가 처음에 S 에 붙어 있었나) · 시드 · 평형 판정 · CN 숫자 · 스핀 (닫힌 껍질로 보임) · 수렴 기준 |

> 관측창 (우리 규칙 `D-2026-10-05-md-observation-window`): AIMD 300 K · 궤적 15 ps · 반응 기회 n = 6 (상자 속 Li⁺ 6 개 — 하나하나가 S 와 붙고 떨어질 기회) · ν₀ 10¹³ s⁻¹ **가정** · 정상성 가정 → 기대 사건 1 ≈ **0.18 eV** (검출 63 %) · 95 % 검출 ≈ **0.15 eV**. 통계 구간 5 ps 만 세면 ≈0.15 / ≈0.12 eV. Li–S 접촉 이온쌍이 풀리는 장벽이 이보다 크면 `Fig. 3f` 의 '짝짓기 성향' 은 Packmol 초기 배치의 기억일 수 있다.

---

## 5. 결과 — 절별 상세 (그림 실독 포함 · 모든 수치)

### 5.1 설계 근거 — 용매 물성 · Li⁺ 결합 (`Fig. 1`, `Fig. S1`, `Fig. S2`, `Table S1`)
- **`Fig. 1a`** (모식도 · 실독): 위 Li 금속 + 'Inorganic enriched SEI' (색 블록 층) · 가운데 'Weak solvation' · 'Intermolecular interactions' (MtBE 분자 두 개 사이 초록 화살표) · 아래 'Suppressed LiPS dissolution' · 양극 표면 'β-S₈ → α-S₈' 화살표. 범례 DOL · DME · Li⁺ · TFSI⁻ · MtBE · S₆²⁻. 개념도이고 데이터는 없다.
- **`Fig. 1b`** (실독): x = 용매 (범주) · y = 밀도 0.7–1.1 g cm⁻³ · 원 크기 = 점도 (범례 0.270 · 0.435 · 0.600 cP) · 배경 노랑 'ε_r > 5' (DME · DOL) · 파랑 'ε_r < 5' (MtBE · CPME · SBME · TAME). DOL ≈1.06 · DME ≈0.87 · CPME ≈0.86 · TAME ≈0.77 · SBME ≈0.74 · MtBE ≈0.74 (가장 작은 원). ⚠ SBME · TAME 의 ε 는 `Table S1` 에 N/A 인데 그림은 'ε_r < 5' 칸에 넣었다 · SBME 점도는 임의 0.4.
- **`Fig. 1c` · `Fig. S2`** (실독): '0.5 M Li₂S₆ in DOL' 에 MtBE 를 +20 % (5:1) · +40 % (5:2) · +60 % (5:3) · +80 % (5:4) · +100 % (1:1) **더한** 바이알 사진 여섯. 색이 검붉은색 → 주황으로 옅어진다. 침전 · 상 분리는 사진에서 안 보인다. 본문은 이것을 "LiPS 용해도가 훨씬 낮다" 의 근거로 쓴다 (§10-②).
- **`Fig. 1d,e`** (실독): Li⁺–용매 결합 막대 — DME **0.643** (양쪽 O 로 1.998 · 1.990 Å) · DOL ≈0.275 (1.946 Å) · MtBE ≈0.15 (2.555 Å) · CPME **≈0.325** (1.921 Å) · SBME ≈0.13 (2.570 Å) · TAME ≈0.15 (2.560 Å). 본문: CPME 는 O 한쪽의 오원환이 입체 장애를 덜 줘서 DOL 보다 조금 세다. MtBE · SBME · TAME 그림에서 Li⁺ 는 O 에서 점선으로 2.55–2.57 Å 떨어져 있다.
- **`Fig. S1`** (접촉 시트): 여섯 분자의 ESP 등면 — DME · DOL 의 O 쪽 음전위 (파랑 · 이 그림의 색 규약) 가 넓고, 단일 산소 에테르는 메틸 · tert-butyl 에 가려져 있다. 정량 값 없음.

### 5.2 Li⁺ 용매화 — 분광 (`Fig. 2a–c`, `Fig. S3`, `Fig. S4`, `Fig. S5`)
- **Raman** (`Fig. S3` 실독): S–N–S 띠 중심 기준 741.6 → MSE 742.5–743.1 cm⁻¹ (본문). 그림은 각 계에 회색 두 성분 (≈740 · ≈745) 맞춤 · MtBE 는 ≈725, TAME 은 ≈708 cm⁻¹ 에 용매 자체 띠가 있다. 이동 폭 1–1.5 cm⁻¹ 이고 장비 분해능 · 맞춤 조건 · 성분 면적비 숫자는 없다. 저자: "CIP/AGG ≈745 cm⁻¹ 성분 세기가 뚜렷이 는다".
- **⁷Li NMR** (`Fig. 2a` 실독): x 축 −0.9 ~ −1.4 ppm · LiPF₆ 기준 점선 ≈ −1.06. 기준 −1.19 (본문) → SBME ≈ −1.10 · MtBE ≈ −1.11 (화살표) · TAME ≈ −1.125 · CPME ≈ −1.17. 저자 해석: 음이온 짝 증가 (가림) 와 Li⁺–용매 약화 (벗김) 가 경쟁하는데 Raman 상 짝 증가는 모든 MSE 에 비슷하므로, MtBE · SBME 의 큰 저자장 이동은 **DME/DOL 을 Li⁺ 에서 더 잘 떼어 낸다**는 뜻.
- **¹⁹F NMR** (`Fig. S4` 실독 · 손 크롭): TFSI⁻ −80.17 → MtBE ≈ −80.21 · TAME ≈ SBME ≈ −80.27 · CPME ≈ −80.31 (봉우리 두 갈래). 이동 폭 0.04–0.14 ppm. 저자: MtBE 의 이동이 가장 작음 → **MtBE 의 H 와 TFSI⁻ 의 상호작용**.
- **¹⁹F DOSY** (`Fig. S5` 접촉 시트): log D DOL/DME ≈ −9.30 (5.01 × 10⁻¹⁰) · MtBE ≈ −9.36 (4.37 × 10⁻¹⁰) · 화학 이동 ≈ −80.18 · ≈ −80.21. 저자: TFSI⁻ 가 조금 느리다 → 용매–음이온 상호작용 증거.
- **¹H NMR** (`Fig. 2b,c` 실독): (b) 순수 DOL/DME → MtBE 추가 → MtBE + 염. DOL 두 봉우리 (≈4.8 · ≈3.85 ppm) · DME 두 봉우리 (≈3.47 · ≈3.30) · MtBE 두 봉우리 (≈3.2 · ≈1.15). 이동은 수백분의 일 ppm 규모 (figure-read). 저자: MtBE 의 O 가 DOL/DME 의 H 전자를 당겨 저자장 이동 → 염을 넣으면 DME 가 Li⁺ 와 짝을 지어 MtBE 봉우리가 고자장으로. (c) 염이 든 다섯 전해질 — MSE-MtBE 의 DME · DOL 봉우리가 가장 저자장 → "MtBE 가 DME/DOL 의 전자 밀도를 가장 많이 줄인다".

### 5.3 계산 — 고전 MD 배위 · DME–용매 결합 · SAXS (`Fig. 2d,e`, `Fig. S6`, `Fig. S7`, `Fig. S8`)
- **`Fig. 2d`** (실독): Li⁺–O_DME 누적 CN (오른쪽 축 2.0–4.5) — 첫 껍질 평탄 (≈2.2–4.5 Å) 에서 DOL/DME ≈3.6 · CPME ≈3.25 · TAME ≈3.15 · SBME ≈3.08 · **MtBE ≈3.03** (최저). 본문 "first solvation shell (∼2–4 Å)". 즉 DME 가 ≈1.8 분자 (두 자리) → ≈1.5 분자.
- **`Fig. S7`** (실독): Li⁺–O_X g(r) 첫 봉우리 ≈1.87 Å · CN 평탄 SBME ≈0.20 · MtBE ≈0.18 · CPME ≈0.09 · TAME ≈0.085. 저자: "limited, yet not negligible, solvating power". (CN 0.2 = Li⁺ 다섯에 하나꼴로 공용매 O 한 개)
- **`Fig. S6`** (접촉 시트): 다섯 계 MD 상자 스냅숏 — 시각적으로 구별되는 군집은 없다.
- **`Fig. 2e`** (실독): DME–X 이량체 결합 DOL ≈0.168 · **MtBE 0.189** · CPME ≈0.174 · SBME ≈0.185 · TAME ≈0.182 eV (y 축이 0.14 에서 시작해 차이가 커 보인다). 저자: "MtBE 의 분자간 상호작용이 가장 강하다".
- **SAXS** (`Fig. S8` 실독 · 손 크롭): (a) I(q) 로그–로그 — 두 계 모두 q ≈1.4–1.5 Å⁻¹ 주 봉우리 (분자 크기 · 분자간 거리) · DOL/DME 는 ≈0.6–0.8 Å⁻¹ 어깨 · MSE 는 0.5–1 Å⁻¹ 이 더 높고 **q < 0.4 Å⁻¹ 에서 ≈0.02 → ≈0.030 으로 계속 오른다** (DOL/DME 는 ≈0.012 로 평평). (b) 같은 자료를 d = 2π/q 로. 저자: 0.6 Å⁻¹ (≈10 Å) = CIP/AGG · 0.05–0.4 Å⁻¹ (수십 nm) = 용매–용매 상호작용으로 인한 큰 규모 군집. ⚠ 절대 세기 보정 · 배경 · 모세관 정보가 없어 저 q 상승이 시료 차이인지 장치 · 배경 차이인지 판단 불가.

### 5.4 Li 음극 쪽 — 동역학 · CE · 대칭셀 (`Fig. 2f–h`, `Fig. S9`–`S12`)
- **Tafel** (`Fig. S9` 실독 · 손 크롭): (a) log\|i\| 대 ±100 mV — DOL/DME 곡선이 다른 넷보다 전 구간 ≈0.3 아래 · (b) i₀ 막대 ≈0.19 · ≈0.425 (MtBE) · ≈0.378 (CPME) · ≈0.40 (SBME) · ≈0.382 (TAME) mA cm⁻². 본문 수치 없음.
- **온도별 EIS** (`Fig. S10` 실독 · `Fig. S11` 접촉 시트): 0–50 °C · 0 °C 반원 폭 DOL/DME ≈760 · MtBE ≈450 · CPME ≈600 · SBME ≈680 · TAME ≈590 Ω · DRT 주 봉우리 τ ≈10⁻³ s 근처 (본문 "10⁻⁴ ~ 10⁻² s") → Rct (탈용매화 전하 이동, 저자 귀속).
- **`Fig. 2f`** (실독): ln R 대 1000/T (3.10–3.66 → 50–0 °C) · 점 6 개 · Ea DOL/DME **64.3** · MtBE **63.6** · CPME **67.3** · SBME **66.5** · TAME **66.0** kJ mol⁻¹. 저자: Rct 는 MSE 가 '훨씬 낮다' (예: 0 °C ln R ≈6.5 대 ≈6.0 → ≈1.6 배) · Ea 는 '비슷' → "주 장벽은 여전히 Li⁺–DME 해리 · 강결합 DME 의 수가 지수 앞 인자와 전체 Rct 를 정한다" · "MtBE 는 실제로 최소 Ea → 짝의 수뿐 아니라 세기도 줄인다".
  > 홉 수 검산 (우리 규칙 `D-2026-09-27-barrier-hop-count` · 겉보기 Arrhenius 기울기라 단일 홉 장벽이 아니다 — 차수만): 64.3 kJ mol⁻¹ = 0.666 eV · 298 K · ν₀ 10¹³ s⁻¹ **가정** → Γ ≈55 s⁻¹ · 1/Γ ≈18 ms. DRT 봉우리 τ ≈1–3 ms (0 °C) 와 차수가 크게 어긋나지 않는다.
- **Aurbach CE** (`Fig. 2g` · `Fig. S12` 실독): DOL/DME **98.0 %** · MtBE **99.5 %** · CPME **99.4** · SBME **98.7** · TAME **98.9 %**. 두 그림의 전압 곡선은 거의 겹친다 · 마지막 박리 끝 시각 ≈59 h (DOL/DME) 대 ≈60 h (MtBE).
- **`Fig. 2h`** (실독): 1 mA cm⁻² · 1 mAh cm⁻² · 600 h. MtBE ±≈0.04 V 로 600 h · DOL/DME 는 ≈300 h 부터 분극이 서서히 커지고 ≈400 h 부터 진동 (+0.4 V 넘게) · ≈540 h 에서 그림이 끝난다. 본문 "slightly lower overpotential" · "failed after 400 h". 셀 하나씩.

### 5.5 폴리설파이드 용매화 — NMR · DOSY · AIMD (`Fig. 3a–f`, `Fig. S13`, `Fig. S14`)
- 저자 전제: MSE 도 LiPS 용해도는 낮지만 **녹는 LiPS 를 거치는 경로**다 (`Fig. S13` — MSE-MtBE 3.7 mg cm⁻² 화성 곡선: 위 평탄 ≈2.33 V → ≈300 mAh g⁻¹ 에서 둘째 평탄 ≈2.12 V · 방전 ≈1270 · 충전 ≈1340 mAh g⁻¹ figure-read · 전형적 두 평탄).
- **`Fig. 3a`** (실독): 0.1 M Li₂S₆ (다른 염 없음) ⁷Li — DOL/DME ≈0.17 · MtBE ≈0.28 (화살표) · SBME ≈0.26 · TAME ≈0.23 · **CPME ≈0.15 (기준보다 고자장)**. 본문: "MtBE 0.28 · 다른 MSE 도 저자장 (CPME 빼고)" → Li⁺–S₆²⁻ 짝 증가.
- **`Fig. 3b,c`** (실독): ¹H DOSY (DME 양성자) log D −8.90 → −8.72 · ⁷Li DOSY −9.35 → −9.25 → D(DME) **1.26 → 1.91 × 10⁻⁹** · D(Li⁺) **4.47 → 5.62 × 10⁻¹⁰** m² s⁻¹. 저자: 용매–Li⁺ 결합 약화 + MtBE 저점도 → 실제 셀의 빠른 물질 이동. ⚠ 전해질 σ 는 반대로 MSE 가 39 % 낮다 (`Fig. S21`) — 이 DOSY 는 **염 없는 Li₂S₆ 용액**이다.
- **AIMD** (`Fig. 3d,e` · `Fig. S14` 실독): DOL/DME 스냅숏 — S₆²⁻ 사슬이 펴져 있고 Li⁺ 는 DOL/DME O 에 둘러싸여 S 와 떨어져 있다 (그림의 녹색 구 2–3 개 중 S 직접 접촉은 거의 없다). MSE-MtBE — S₆²⁻ 가 고리 모양으로 접혀 Li⁺ ≈3 개가 S 와 직접 닿은 덩어리 · 그 주변에 TFSI⁻ · NO₃⁻ 도 붙어 있다 (`Fig. S14` 상자 전체 그림). 
- **`Fig. 3f`** (실독): S(S₆²⁻)–Li⁺ g(r) — 첫 봉우리 r ≈2.5 Å · MSE ≈22 대 DOL/DME ≈15 · 둘째 ≈3.6 Å 에서 ≈7 대 ≈4 · 6 Å 밖 ≈1. 저자: MtBE 가 Li⁺–S₆²⁻ 짝을 늘리고 DME 를 Li⁺–S₆²⁻ 착물의 안쪽 껍질에서 끌어낸다 (DME 수 · CN 숫자는 안 냈다).
- 결론 문장: "MSE-MtBE 가 폴리설파이드 용매화를 이온쌍 쪽으로 가장 효과적으로 옮긴다 → 이후 평가는 MSE-MtBE 로".

### 5.6 셔틀 · 분극 · 핵생성 · 액–액 전하 이동 (`Fig. 3g–i`, `Fig. S15`–`S22`)
- **셔틀 전류** (`Fig. S15` 실독): 2.25 V (고차 LiPS 가 거의 다 생긴 지점) 유지 10 h. DOL/DME — 곧바로 양 (산화) 전류로 바뀌어 ≈0.072 mA 정점 → **0.047 mA** · MSE — −0.1 mA (환원) 에서 천천히 올라 ≈1 h 에 0 을 지나 ≈0.018 → **0.013 mA**. 저자: 느린 전류 변화 = 셔틀 억제.
- **GITT-EIS** (`Fig. 3g` · `Fig. S16` 실독): (a) GITT 전압 — 위 평탄 (≈2.35 → ≈2.3 V) 이 ≈8 h · 둘째 평탄 ≈2.13 V · 기준은 ≈38 h · MSE 는 ≈39.5 h 에 끝 (figure-read). (b) η_ohm 정점 ≈25 % DOD 에서 **2.81 대 2.10 mV** (LiPS 농도 최대 = 핵생성점) · 끝 ≈1 mV. (c) η_act 정점 **19.5 대 10.4 mV** (MSE 가 큼 — 저자: LiPS 농도↓ → 핵 · 핵자리↓) · 40 % 뒤 둘 다 ≈6–7 mV. (d) η_conc ≈25 % 에서 **44.7 대 47.4 mV** (MSE 가 조금 작음 — 저자: 쉬운 LiPS 이동 · 낮은 탈용매화 에너지) · 84–92 % DOD 에서 MSE 가 훨씬 작다 (≈47 대 ≈75 · ≈55 대 ≈203 · ≈158 대 ≈305 mV) · 96–100 % 는 비슷 (≈358 대 ≈390 · 둘 다 ≈435). 저자: 끝 구간 낮은 η_conc = 좋은 젖음 (`Fig. S17`) · 고른 석출. **η_total** (`Fig. 3g`) 은 ≈25 % 에서 ≈65 mV 정점 · 평탄 ≈45 mV · 기준은 0–20 % DOD 에서 오히려 작다 (≈20–28 대 ≈38–58 mV).
- **젖음** (`Fig. S17` 접촉 시트): 0 ms 두 방울 모두 구형 · 25 ms 에 MSE 방울이 더 넓게 퍼져 양극에 스며든 모양. 사진 한 쌍 · 정량 없음.
- **정전위 Li₂S 석출** (`Fig. S18` 실독): Li₂S₈ · 2.08 V · 5 h. DOL/DME 정점 ≈0.70 mA at **0.266 h** · 면적 **161 mAh g⁻¹** · MSE 정점 ≈1.06 mA at **0.234 h** · **232 mAh g⁻¹** (짙은 띠 = 빼낸 배경으로 보인다). 저자: "정점 시간이 비슷 → 같은 LiPS 농도에서는 MSE 가 핵생성 속도를 해치지 않는다 · 실제 셀에서는 용해도 차이로 핵생성이 바뀔 수 있다". 정점 시간은 MSE 가 12 % 빠르다.
- **Li₂S₆ 대칭셀** (`Fig. 3h,i` · `Fig. S19`–`S20` 실독/접촉 시트): DRT (MSE, `Fig. 3h`) — 0 °C 주 봉우리 τ ≈0.1 s (γ ≈16 Ω) → 온도가 오르면 ≈3 × 10⁻³ s 쪽으로 이동 · 별도 봉우리 ≈10⁻⁶ s 와 ≈0.3 s (40–50 °C). DOL/DME DRT (`Fig. S20`) 0 °C 봉우리 ≈0.07 s (γ ≈12.3). x 축 라벨이 'tau (Ω)' (단위 오기 — `Fig. 3h` · `Fig. S20`). Nyquist (`Fig. S19`) 0 °C 반원 ≈17 대 ≈32 Ω · 고주파 절편 ≈2.5 대 ≈5 Ω. **`Fig. 3i`**: ln Rct · Ea **44.4 (DOL/DME) 대 41.1 (MSE) kJ mol⁻¹** · Rct 는 전 온도에서 MSE 가 높다. 저자: 장벽은 MSE 가 낮지만 전체 속도는 낮은 σ 때문에 느리다.
  > 홉 수 검산 (차수만 · 겉보기 기울기): 41.1 kJ mol⁻¹ = 0.426 eV · 298 K · ν₀ 10¹³ s⁻¹ **가정** → Γ ≈6 × 10⁵ s⁻¹ · 1/Γ ≈1.6 µs. DRT 봉우리 τ (ms–0.1 s) 와는 3–5 자릿수 차이다 — 이 Ea 를 '원자 한 번의 탈용매화 장벽' 으로 읽으면 안 된다는 뜻이다 (지수 앞 인자에 자리 수 · 농도 · 면적이 다 들어간다).
- **CV** (`Fig. S22` 접촉 시트): Li₂S₆ 대칭 5 mV s⁻¹ 5 사이클 — DOL/DME 봉우리 ±≈15–16 mA · MSE ±≈10 mA · MSE 곡선이 사이클 간 더 잘 겹친다 (본문 "slightly lower, but more reversible").

### 5.7 operando · ex situ XRD — S₈ 다형 (`Fig. 4`, `Fig. S23`)
- **`Fig. 4a,b`** (실독): 왼쪽 전압–시간 (C/25) · 오른쪽 2θ 21–30° 등고선. 
  - 두 계 모두 처음 α-S₈ 반사 (■: ≈22.0 · 22.8 · 23.1 (가장 강함) · 25.9 · 26.8 · 27.8 · 28.7 · 29.0°) 가 방전 3–5 h 안에 사라진다. Li₂S 는 ≈27° 의 넓은 띠로 방전 후반–충전 초반에 보인다 (흐림). 두 계 모두 ≈25.6–26° 에 처음부터 끝까지 이어지는 세로 줄이 있다 (셀 부품으로 보인다 · 논문 언급 없음).
  - 방전 끝 figure-read: MSE ≈16.5 h · ≈1.65 V / 기준 ≈17 h · ≈1.7 V. C/25 를 1500 mA g⁻¹ 기준 60 mA g⁻¹ 로 놓으면 방전 ≈990 · ≈1020 mAh g⁻¹ 정도 (**우리 산수** · 휴지 없음 가정).
  - 충전 끝 (점선 위): **DOL/DME** — ≈28–29 h 부터 β-S₈ (◆ 8 개: ≈23.4 · 23.6 · 24.1 · 25.3 · 26.0 · 26.8 · 27.7 · 28.4°) 만. **MSE-MtBE** — ≈28 h 에 β-S₈ (◆ 4 개: ≈23.7 · 24.1 · 25.3 · 26.1°) → ≈30–31 h 부터 α-S₈ (■) 가 나타나 충전 끝 (≈34 h) 에 23.1° 반사가 처음만큼 강하다.
  - 저자: β-S₈ 는 용매화된 LiPS 에서 먼저 핵생성 (동역학적으로 유리) · 열역학 안정상 α-S₈ 는 준고체 반응이 켜질 때 자란다 — 'MSE 특유의 두 단계 S 석출'.
- **`Fig. S23`** (실독): DOL/DME 1 사이클 뒤 양극 — β-S₈ (◆ ≈24.0 · 25.2 · 25.9 · 28.2 · 34.1°) · 같은 전극을 MSE-MtBE 에 담근 뒤 — α-S₈ (■ ≈23.0 (강) · 25.8 · 26.6 · 27.4 · 31.2 · 34.0 · 36.9°). 두 패턴 모두 ≈18° 에 넓은 언덕 (탄소 · 결합제 · 분리막). 저자: MSE 가 고차 LiPS ⇌ 원소 S 균형을 바꿔 용해–재석출로 β-S₈ 를 α 로 바꾼다 → 충전 동역학을 지키면서 LiPS 용해를 최소화하는 핵심 기전일 수 있다.

### 5.8 셀 성능 (`Fig. 5`, `Fig. S24`–`S28`, `Table S2`)
- **저하중** (`Fig. S24` 실독 · 2.2 mg cm⁻² · E/S 18 · C/3): MSE 945 → 711 (75.2 %) · 기준 ≈905 → 537 (59.3 %). 기준은 ≈40–60 cyc 에 ≈680 으로 내려갔다가 ≈62 cyc 에 ≈710 으로 계단 상승.
- **`Fig. 5a`** (실독 · 3.7 mg · E/S 10 · C/5 · 180 cyc): MSE 화성 ≈1280 · ≈1130 · ≈1040 · ≈1010 → C/5 ≈890 → **710** · 기준 ≈1190 · … → C/5 ≈810 → **458** (≈120 cyc 부터 꺾여 내려감).
- **C/10 장기** (`Fig. S25` 접촉 시트): 1,019 → 848 (83.2 %, 140 cyc).
- **율** (`Fig. 5b` 600 dpi 확대 · `Fig. 5c` · `Fig. S26`): 각 율 10 사이클 · 0.1–0.5C → 0.2C 복귀. 판독값은 §3d. 본문: "C/2 에서 781 · 기준 700 → 10 cyc 뒤 < 550 · 복귀 C/5 에서 ≈850 대 < 700 · 과전압은 C/2 핵생성점의 더 큰 패임 말고는 비슷". 복귀 율은 그림 라벨로는 '0.2C' (본문은 'C/5' = 같은 값).
- **45 °C** (`Fig. 5d,e` · `Fig. S27` 실독): 기준 화성 첫 CE **38.5 %** — `Fig. 5e` 에서 충전이 ≈2.30 V 평탄으로 1600 mAh g⁻¹ 를 넘게 이어지며 시간 제한 전에 2.8 V 에 못 닿는다 (전형적 셔틀). C/5 첫 **770** → 90 cyc **627** · CE ≈30 cyc 부터 떨어져 평균 **89.4 %** (그림: ≈91.5 → ≈83.5 %). MSE 화성 첫 CE **79.7 %** (본문) · 90 cyc **799** · 평균 CE **94.6 %** (그림 ≈94–95.5 %). `Fig. S27` 주석: 다른 MSE 도 시험했고 MtBE 가 CE 최고 · CPME 최저 (≈93 → ≈88 % · 흩어짐 큼) — "⁷Li NMR 이동 순서와 CE 순서가 맞는다 → 용매화 구조와 성능의 상관".
- **파우치** (`Fig. 5f` · `Fig. S28`): 3.5 mg · E/S 5.5 · C/10 70 cyc 768 · 4.6 mg · E/S 4.5 · C/20 20 cyc 779. 
- **`Table S2`** (글자층): 문헌 MSE/WSE 8 편과 비교 — 예: BDTS–LiTFSI–CPME (Pang · 55 °C C/5 · 2 mg · E/S 5 · 150 cyc 680 → 620 코인 · 40 °C 4 mg · E/S 3 · 24 cyc 1140 → 740 파우치) · G2–0.8LiTFSI (25 °C · 3 mg · E/S 5 · 10 cyc 1422 → 1410 파우치) · 1.0M-DMFN (C/7.5 · 4 mg · E/S 8 · 300 cyc 770 → 604) · DME-TFTFE (0.15 C · 3.8 mg · E/S 5 · 154 cyc 900 → 600) · 이 논문 코인 (C/5 · 21 °C · 3.7 · E/S 10 · 180 cyc 894 → 710) · 파우치 (C/20 · 4.6 · E/S 4.5 · 20 cyc 773 → 779). ⚠ E/S · 온도 · 율 · 사이클 수가 다 달라 한 줄 비교가 안 되는 표다 — 이 논문 코인의 E/S 10 은 표에서 가장 넉넉한 축이다.

### 5.9 계면 — SEM · XPS (`Fig. 6`, `Fig. S29`)
- **SEM** (`Fig. S29` 접촉 시트): Li\|S 30 사이클 뒤 Li — MSE 조밀한 큰 알갱이 + 얇은 금 (배율막대 10 µm) · DOL/DME 틈이 많은 덩어리 (배율막대 **20 µm** — 두 그림 배율이 다르다).
- **Li 음극 S 2p** (`Fig. 6a` 실독): 귀속 SO₄²⁻/─SO₂ 168.7 · SO₃²⁻/─SO 167.1 · S_B⁰ 163.6 · S_T⁻¹ 161.6 · S⁻² 159.9 eV (각 2p₃/₂ · 본문). 그림: MSE 는 SOₓ 영역 (166–170 eV) 이 가장 크고 SO₃ 성분 (파랑 · ≈167.3) 이 뚜렷 · 기준은 S_B⁰ (≈163.8) 가 가장 큰 봉우리 · S⁻² (≈159.9) 도 뚜렷. 저자: 산화 S (LiNO₃ 가 관여한 LiTFSI 분해 + LiPS 산화) 가 부동태 · 환원 S (LiPS 이동) 는 셔틀 지표 · MSE 의 산화 S 는 결합에너지가 조금 낮다 → 부동태층 전도도에 유리할 수 있다.
- **Li 음극 F 1s** (`Fig. 6b` 실독): C–F ≈688.7 · Li–F ≈684.7 eV (본문). 높이비 Li–F/C–F figure-read MSE ≈1.0 · 기준 ≈0.5.
- **깊이 분석** (`Fig. 6c` 실독): 스퍼터 0–11 min · S 2p 와 F 1s 등고선 넷. 기준 S 2p 는 ≈6 min 뒤 ≈160 eV (S²⁻) 쪽이 빨강으로 커진다 · MSE 는 ≈167 eV (SOₓ) 가 내내 빨강. F 1s — MSE 는 Li–F (≈685) 가 내내 빨강 · 기준은 표면 0–1 min 에 C–F (≈688.5) 가 빨강이고 안쪽에서 Li–F 가 노랑. ⚠ 색 막대에 숫자가 없다 — 지도마다 따로 정규화했으면 시료 사이 세기 비교는 안 된다 (§10-⑫).
- **충전 상태 양극** (`Fig. 6d,e` 실독): S 2p — MSE 는 원소 S⁰ (164.5 eV · 보라) 가 가장 크다 · 기준은 S_B⁰ (분홍 · ≈163.4) 가 가장 크고 SO₄²⁻ (≈169) 도 크다. 저자: 기준은 LiPS 생성이 많아 비활성 S · 전해질 분해 · 양극–음극 교차 · MSE 는 원소 S 비율↑ (XRD 와 일치). F 1s Li–F/C–F 높이비 figure-read MSE ≈0.5 · 기준 ≈0.2.

---

## 6. 메커니즘 · 논증 흐름 (`Fig. 1a`) — 사슬 판정

저자의 논증은 두 갈래가 한 전해질에서 같이 생긴다는 그림이다:

> **(Li 음극 갈래)** 단일 산소 에테르 30 % → Li⁺–DME 배위↓ (CN 3.6 → 3.0) + 양이온–음이온 회합↑ (Raman · NMR) → 탈용매화 쉬움 (Rct↓ · i₀↑) → 음이온 유래 LiF 풍부 SEI (XPS) → CE 99.5 % · 600 h.
> **(양극 갈래)** 같은 용매화 변화 → LiPS 용해↓ + Li⁺–S₆²⁻ 짝↑ (AIMD) + 젖음↑ + DME 확산↑ (DOSY) → 셔틀↓ (0.047 → 0.013 mA) · η_conc↓ (방전 끝) → 충전 끝 β → α S₈ (operando XRD) · 원소 S 회수↑ (XPS) → 사이클 · 45 °C 안정성.

| 단계 | 주장 | 근거 | 판정 |
|---|---|---|---|
| ① | MSE 가 Li⁺–DME 배위를 줄인다 (MtBE 가 가장) | 고전 MD CN · ⁷Li 저자장 이동 · ¹H 저자장 이동 | ✅ 방향 · ⚠ '왜 MtBE 인가' 의 크기 (CN ≈3.03 대 CPME ≈3.25 · 시드 1 · 오차 없음) |
| ② | 양이온–음이온 회합이 는다 | Raman 1–1.5 cm⁻¹ · ¹⁹F 고자장 · SAXS 0.6 Å⁻¹ | ✅ 정성 — 그러나 **강용매 대비 염 1.43 배** 만으로도 같은 방향이 나온다 (대조군 없음 — §10-①) |
| ③ | 용매–용매 상호작용 (MtBE–DME 0.189 eV 최대) 이 DME 를 Li⁺ 에서 끌어낸다 | `Fig. 2e` DFT · ¹H 이동 | 🔴 이량체 차 0.021 eV ≈0.8 kT · BSSE · 기준 (DME–DME) 없음 · Li⁺–DME 0.643 eV 와 비교하면 한 자릿수 작다 |
| ④ | 탈용매화 장벽이 낮아진다 | `Fig. 2f` Ea | 🔴 MtBE 만 −0.7 kJ mol⁻¹ (오차 없음) · 나머지 셋은 +1.7–3.0 kJ mol⁻¹ **높다** · Rct↓ 는 지수 앞 인자 (자리 수 · 면적) 쪽 |
| ⑤ | LiF 풍부 SEI → Li 안정 | XPS 높이비 · CE · 대칭셀 · SEM | ✅ 방향 (셀 · 시료 각 1 · 세척 미기재) |
| ⑥ | LiPS 용해가 제한된다 | 사진 (`Fig. 1c` · `Fig. S2`) · 셔틀 전류 | 🔴 용해도 수치 없음 · 사진은 희석과 섞임 · 1:1 에도 침전 없음 → 셔틀 감소의 원인으로 '용해도' 와 '확산 · 이온쌍' 을 못 가른다 |
| ⑦ | Li⁺–S₆²⁻ 짝이 는다 | ⁷Li (Li₂S₆ 용액) · AIMD g(r) | ⚠ NMR 정성 ✅ · AIMD 는 S₆²⁻ 1 개 · 15 ps · 궤적 1 (관측창 ≈0.18 eV) |
| ⑧ | 충전 끝 β → α (MSE 특유의 두 단계 석출) | operando XRD · ex situ 담금 | ⚠ 관찰은 실제 · 'MSE 때문' 은 대조 (DOL/DME 담금 · 같은 시간 방치) 없이 미확정 — β-S₈ 의 자발 전이 가능성 (§10-⑥) |
| ⑨ | 실용 성능 | 코인 · 45 °C · 파우치 | ✅ 사이클 유지율 · 45 °C CE · ⚠ 율 숫자 (781) · 첫 CE (79.7) 가 그림과 다름 · 파우치 소형 |

**빠진 대조군 (가장 큰 교락)**: MSE 의 효과 대부분이 **'강용매를 30 % 덜어 낸 희석'** 만으로도 설명될 수 있다. 1 M 염을 유지한 채 DOL+DME 를 70 % 로 줄이면 강용매당 염이 1.43 배가 되어, 비용매 희석제 (예: 불소 에테르 · LHCE) 를 넣었을 때와 같은 방향 (접촉 이온쌍↑ · 음이온 유래 LiF SEI · Li CE↑) 이 나온다. 이 논문이 'MtBE 의 용매–용매 상호작용' 을 따로 증명하려면 ① 같은 부피 비율의 비용매 희석제 MSE ② DOL/DME 에서 염 농도만 1.43 M 으로 올린 전해질 중 하나는 있어야 했다. 넷의 MSE 사이 차이 (CE 98.7–99.5 % · Ea 63.6–67.3) 는 그 '희석 공통 효과' 위의 작은 변주다. 이 교락은 shen2026 의 '같은 σ 대조군 부재' 와 같은 꼴이다 (`papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md` §6).

---

## 7. 우리 계산 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

> 규율: 문헌 수치는 소환값이다 — 이 논문의 숫자와 우리 절대값을 한 표에 놓지 않는다. 이 논문은 **액체 전해질**이라 A–D 물성 4축 비교 행이 없다. 아래는 **방법**과 **개념**만 맞댄다.

### 7a. 방법 대조 — 같은가 다른가

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| MD 의 힘 (배위 · 구조) | 고전 OPLS-AA (용매 1.2*CM5 · 이온 0.8 배 축소 전하 · 비분극) · 5 계 · 1300–1400 분자 | UMA-s-1p1 (`omat`) MLIP-MD — 결정 LPSCl 계 · 우리 Ea · D 는 **AIMD 도 고전 MD 도 아니다** (`our_dft_baseline.md` 머리 주의) | 힘 계산 축이 셋 다 다르다. 고전 MD 배위수는 전하 축척 선택에 민감하다 (전하 0.8 배 ↔ 1.0 배면 Li–음이온 짝 정도가 달라진다) — 계산 전에 무엇에 맞췄는지 적어야 한다 |
| MD 의 힘 (폴리설파이드) | VASP PBE AIMD (분산 보정 미기재) · 512 / 505 원자 · 15 ps · Γ · 삼중수소 질량 · 1 fs | 해당 없음 | 보고량이 다르다 (용액 구조 g(r) ↔ 우리 결정 수송 MSD) — 수치 대조 없음 |
| 표본 · 통계 | 고전 MD 계마다 1 궤적 (마지막 5 ns) · AIMD S₆²⁻ 1 개 · 5 ps 통계 · 시드 미기재 · 오차 막대 0 | 우리 규칙: **비율도 멀티시드 판정만** (단일시드 1.33× 철회 사례) | 이 논문의 CN(O_DME) 3.03 대 3.25 순위는 우리 기준으로 '한 번의 관측' 이다 |
| 짧은 MD 서술의 창 | 없음 | `D-2026-10-05-md-observation-window` | §4e 에 붙였다: 300 K · 15 ps · 기회 6 → Ea₁ ≈0.18 eV (63 %) · Ea₉₅ ≈0.15 eV |
| 분자 DFT | Gaussian 16 · B3LYP-D3(BJ)/6-311+G(d,p) 최적화 + 진동 · M06-2X-D3/ma-def2-TZVP(-f) 단일점 · IEFPCM (용매 미기재) · BSSE · ΔG 미기재 | desktop WSL ORCA **r2SCAN-3c** (SDCP 분자 계열 · opt+freq · 허수 0 확인 — `kb/projects/sdcp_linio2_binding.md`) | r2SCAN-3c 는 gCP 로 BSSE 를 기하적으로 보정한다 (방법 일반 지식). 이 논문 쪽 0.02 eV 규모 차이 (`Fig. 2e`) 는 BSSE · 범함수 · PCM 용매 선택만으로 뒤집힐 수 있는 크기다 (크기 미추정) |
| 결합에너지의 '상태' | Li⁺ 1 개 + 리간드 1 개 (실제 액체 Li⁺ 는 4–5 배위) · 내재 용매 · 세 착물은 Li–O 2.55 Å | 회신 N/O 규율 — admissible state 가 여럿인데 선택 · 집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다 (`CLAUDE.md` 계산 규율 · SDCP 여덟 번 반려 사례) | `Fig. 1d` 는 '어느 배좌 · 어느 배위수의 결합인가' 가 정해지지 않은 스칼라의 외부 사례다 |
| 화학결합 규모 흡착의 배위수 | 해당 없음 (\|E\| ≤ 0.65 eV) | `D-2026-10-05-adsorption-site-coordination` (≳ 2 eV 면 배위수부터) | 규모 밖. 다만 Li⁺ 1 배위 착물은 '맨 Li 포화' 상태라는 같은 경고가 정성적으로 걸린다 |
| 장벽 인용 · 홉 수 검산 | 겉보기 Arrhenius Ea (Rct) 넷 | `D-2026-09-27-barrier-hop-count` | §5.4 · §5.6 에 붙였다 (64.3 kJ mol⁻¹ → 1/Γ ≈18 ms · 41.1 → ≈1.6 µs). 후자는 DRT τ 와 3–5 자릿수 어긋나 '단일 장벽' 으로 못 읽는다 |
| 산화 판단 창 | 해당 없음 (Li–S 1.7–2.8 V) | 우리 양극 쪽 산화 · CEI 판단 창 2.5–4.25 V (NCM 셀용) | 다른 셀이다 — 이 논문 값을 우리 창 판단에 쓰지 않는다 |

### 7b. 개념 대조 — 우리 계와 닿는 곳

- **'희석제가 Li⁺ 껍질에서 강용매를 빼낸다' 는 LHCE 의 일반 논리다.** 이 논문은 비불소 · 저밀도 '약한 용매' 를 희석제로 쓴 판이고, 그 결과 (CIP/AGG↑ · LiF↑ · CE↑) 는 우리가 SEI 트랙 · XPS 동정 기준표 (`db/properties/xps_reference_sei.csv` · 위치만) 를 읽을 때 '음이온 유래 SEI' 판단의 문헌 쪽 예시로만 닿는다. 우리 황화물 SE | Li 계면에는 용매가 없다 — 이 논리를 그대로 옮기지 않는다.
- **SE 가 산화환원에 낀다 (우리 축 ①)**: 우리 grand-potential 산화 개시는 S²⁻ 가 한계를 정하는 **층①** 값이다 (`our_dft_baseline.md` ESW 절 — 2.256 V · 산물에 원소 S · 창 절대값을 문헌과 맞다고 쓰지 않는다는 단서 포함). 이 논문 셀의 충전 평탄 (≈2.3–2.35 V) · 충전 끝 (2.8 V) 은 그 근처 · 위다. 즉 LPSCl 을 쓰는 전고체 Li–S 에서는 SE 산화가 열역학적으로 허용되는 창에서 셀이 돈다 — 실측 쪽 정본은 `cronk2026_lis_cathode_interphase_chemistry` · `yu2025_cng_host_suppress_argyrodite_oxidation_lis` 다. 이 액체 논문의 전해질 (에테르 · TFSI⁻) 은 그 창에서 반응물로 다뤄지지 않는다.
- **재충전 S 의 다형 (β-S₈ ↔ α-S₈)**: 우리 ESW 반응식의 원소 S 산물은 MP 상 그림에서 고른 S 상이다 (어느 다형인지는 이 digest 에서 확인하지 않았다). 이 논문 · shen2026 둘 다 '실제 셀의 재충전 S 는 준안정 β-S₈ 로 먼저 나온다' 를 보인다 — 열역학 기준상과 **다른 다형**으로 나올 수 있다는 정성 경고로만 가져온다 (우리 판정에 미치는 크기는 재지 않았다).
- **Li₂S**: 이 논문의 Li₂S 는 operando XRD 의 넓은 ≈27° 띠 (저결정) 뿐이다. 우리 SEI 트랙의 Li₂S **결정** NEB (`HZ-sei-neb-li2s-cc-cellconv` · CONDITIONAL) 와 질문이 다르다 — 옆에 두지 않는다. li2s 계열 (LPSCl@Li₂S 소셀 유리 · li2s-2 · li2s-3) 은 2026-11-16 닫혔고 이 논문은 그 재개 사유가 아니다.

### 7c. 🔑 층위를 갈라 쓴 결론 (원고 · 발표용 · 내부)

> **"DOL/DME 의 30 vol% 를 단일 산소 에테르로 바꾸면 Li CE (98.0 → 99.5 %) · 셔틀 전류 (0.047 → 0.013 mA) · 45 °C CE (≈89 → ≈95 %) 가 좋아진다는 것은 이 논문의 실측이 받친다. 그 원인을 'MtBE 의 용매–용매 상호작용 · 낮아진 탈용매화 장벽 · 낮아진 LiPS 용해도' 로 돌린 근거는 (0.02 eV 이량체 차 · MtBE 만 0.7 kJ mol⁻¹ 낮은 Ea · 측정값 없는 용해도) 얇고, 강용매 희석 (염/강용매 1.43 배) 이라는 더 단순한 설명을 가르는 대조군이 없다."**

---

## 8. DFT/계산 방법 ★ (템플릿 항목별 · 상세는 §4e)

- **code / version**: Gaussian 16 (분자) · GROMACS 2024 (고전 MD) · VASP 6.4.2 (AIMD).
- **functional + vdW**: 분자 최적화 B3LYP + D3(BJ) · 단일점 M06-2X + D3 (영 감쇠) · AIMD PBE (분산 보정 **미기재**) · 고전 MD OPLS-AA.
- **pseudo / basis**: 분자 6-311+G(d,p) (최적화) · ma-def2-TZVP(-f) (단일점) · VASP PAW (POTCAR 판 미기재) · ENCUT 550 eV.
- **용매 모형**: IEFPCM (어떤 유전율인지 미기재).
- **k-points / supercell / nat**: AIMD Γ 점만 · 1.8³ / 1.75³ nm³ · 512 / 505 원자 (우리 산수) · 고전 MD 6.5³ nm³ 초기 (NPT).
- **DFT+U**: 없음 (해당 없음).
- **AIMD**: NVT · Nosé–Hoover · 300 K · 15 ps (마지막 5 ps 통계) · 1 fs · H → 삼중수소 질량.
- **고전 MD**: NPT 1 bar · 298 K · 15 ns (마지막 5 ns) · 1 fs · C-rescale / V-rescale · 전하 축척 (용매 1.2*CM5 · 이온 0.8 배).
- **MLIP**: 없음.
- **무질서 처리**: 액체 — Packmol 초기 배치 1 개 (시드 미기재).
- **보고량**: 결합에너지 (전자 에너지 · 내재 용매 · BSSE 미기재 · 부호를 양수로 표시) · g(r) · 누적 CN · 스냅숏 · ESP.
- **특이사항**: `Table S3` TAME 행 '244 MtBE' 는 TAME 의 오기 (우리 부피 검산) · `Fig. 2d` 만 색 규약이 다름 · DFT 결합 순서 (CPME 최대) 와 MD 배위 순서 (CPME 최소) 가 엇갈린다.

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | (a) MSE-MtBE Li–S 모식도 (무기 SEI · 약한 용매화 · 분자간 상호작용 · LiPS 용해 억제 · β-S₈ → α-S₈) (b) 용매 밀도–유전율–점도 지도 (c) 0.5 M Li₂S₆ in DOL 대 +100 % MtBE 사진 (d) Li⁺–용매 결합 DME 0.643 · CPME ≈0.325 · DOL ≈0.275 · MtBE/TAME ≈0.15 · SBME ≈0.13 eV (e) Li⁺–O 거리 (MtBE · SBME · TAME 2.55–2.57 Å) | 1:1 착물 결합에너지의 '상태 미정의' 반례 · 희석과 섞인 용해도 사진의 반례 |
| 2 | (a) ⁷Li NMR −1.19 → MSE 저자장 (b,c) ¹H NMR 용매–용매 (d) 고전 MD CN(O_DME) ≈3.6 → ≈3.0 (MtBE) (e) DME–용매 결합 0.168–0.189 eV (f) Li\|Li Rct Arrhenius Ea 63.6–67.3 kJ mol⁻¹ (g) Aurbach CE 98.0 대 99.5 % (h) Li\|Li 600 h | 고전 MD 배위수 보고 규약 (시드 · 전하 축척) · Ea 차가 오차보다 작을 때의 서술 반례 (MtBE 만 낮음) |
| 3 | (a) Li₂S₆ 용액 ⁷Li 0.17 → 0.28 (CPME 만 고자장) (b,c) DOSY D(DME) 1.26 → 1.91 × 10⁻⁹ · D(Li⁺) 4.47 → 5.62 × 10⁻¹⁰ (d,e) AIMD 스냅숏 — MSE 에서 Li⁺ ≈3 개가 S₆²⁻ 에 붙은 덩어리 (f) S–Li g(r) 봉우리 ≈22 대 ≈15 (g) GITT-EIS η_total (h) MSE Li₂S₆ 대칭셀 DRT (i) Rct Ea 41.1 대 44.4 kJ mol⁻¹ | AIMD 1 음이온 · 15 ps 의 관측창 예시 · 겉보기 Ea 의 홉 수 검산이 DRT τ 와 어긋나는 예 |
| 4 | (a,b) operando XRD (C/25) — 두 계 모두 α-S₈ 소멸 · Li₂S 넓은 띠 · 충전 끝 DOL/DME 는 β-S₈ 만 · MSE 는 β-S₈ → α-S₈ | 상 시간표의 정성 판독 · '두 단계 석출' 귀속에 대조군이 필요한 사례 |
| 5 | (a) 3.7 mg C/5 180 cyc 710 대 458 (b) 율 (C/2 그림 ≈700 · 본문 781) (c) MSE 율별 곡선 (d) 45 °C 90 cyc 799 대 627 (e) 45 °C 첫 사이클 — 기준 2.30 V 끝없는 충전 (셔틀) (f) 파우치 70 cyc 768 | 본문–그림 대조 감사 (율 숫자 · 첫 CE) · 셔틀 판별 (충전 평탄이 끝나지 않음) |
| 6 | (a) Li S 2p — MSE 산화 S · 기준 환원 S (b) Li F 1s Li–F/C–F ≈1.0 대 ≈0.5 (c) 스퍼터 깊이 등고선 (색 막대 숫자 없음) (d,e) 충전 양극 S 2p · F 1s — MSE 원소 S⁰ 우세 | XPS 동정 (SOₓ 168.7 ↔ TFSI⁻ 잔류 겹침 · 세척 미기재) 주의 예 |
| S1 | 여섯 분자 ESP 등면 | 참고 |
| S2 | 0.5 M Li₂S₆ in DOL + MtBE 20–100 % 사진 — 옅어짐 · 침전 없음 | 희석 교락 사례 (용해도 측정 아님) |
| S3 | Raman S–N–S 두 성분 맞춤 · 띠 741.6 → 742.5–743.1 cm⁻¹ · y 라벨 'Absorbance' | 참고 (분율 숫자 없음) |
| S4 | ¹⁹F NMR TFSI⁻ −80.17 → −80.21 (MtBE) … −80.31 (CPME) | 참고 (손 크롭) |
| S5 | ¹⁹F DOSY D 5.01 → 4.37 × 10⁻¹⁰ | 참고 |
| S6 | 고전 MD 상자 다섯 | 참고 |
| S7 | Li⁺–O_X g(r) · CN SBME ≈0.20 · MtBE ≈0.18 · CPME ≈0.09 · TAME ≈0.085 | DFT 결합 순서와 MD 배위 순서가 엇갈리는 예 |
| S8 | SAXS I(q) · I(d) — MSE 저 q 상승 | 절대 세기 보정 없는 SAXS 해석의 한계 (손 크롭) |
| S9 | Li\|Li Tafel · i₀ ≈0.19 (기준) · ≈0.38–0.43 (MSE) mA cm⁻² | 참고 (손 크롭 · 직선 구간 불명) |
| S10 | Li\|Li 온도별 Nyquist 다섯 계 (0 °C 반원 ≈450–760 Ω) | `Fig. 2f` 의 원자료 |
| S11 | Li\|Li DRT 다섯 계 (봉우리 τ ≈10⁻³ s) | DRT 면적 → Rct 관례 |
| S12 | Aurbach CE CPME 99.4 · SBME 98.7 · TAME 98.9 % | 참고 |
| S13 | MSE-MtBE 화성 곡선 — 전형적 두 평탄 (방전 ≈1270 mAh g⁻¹) | 'MSE 도 용액 매개 경로' 의 근거 |
| S14 | AIMD 상자 전체 스냅숏 두 계 | 참고 |
| S15 | 2.25 V 셔틀 전류 0.047 대 0.013 mA | 셔틀 전류 측정법 · 비정규화 단위 (mA) 주의 |
| S16 | GITT-EIS 전압 · η_ohm · η_act · η_conc (DOD 별) | 분극 분해 방법 참고 (식 미기재) |
| S17 | 양극 위 방울 0 / 25 ms 사진 | 참고 (정량 없음) |
| S18 | 정전위 Li₂S 석출 t_m 0.266 대 0.234 h · 161 대 232 mAh g⁻¹ | 조건 미기재 석출 실험의 예 (Scharifker–Hills 맞춤 없음) |
| S19 | Li₂S₆ 대칭셀 Nyquist — MSE 반원이 ≈2 배 | `Fig. 3i` 원자료 |
| S20 | DOL/DME Li₂S₆ DRT (x 라벨 'tau (Ω)') | 참고 |
| S21 | σ 11.68 대 7.11 mS cm⁻¹ | MSE 의 수송 손해 — 개선이 수송이 아니라는 쪽 근거 |
| S22 | Li₂S₆ 대칭 CV 5 mV s⁻¹ | 참고 |
| S23 | ex situ XRD — DOL/DME 사이클 뒤 β-S₈ · MSE 담금 뒤 α-S₈ | 대조 담금 없는 다형 전이 귀속의 반례 |
| S24 | 2.2 mg · E/S 18 · C/3 200 cyc 711 대 537 | 참고 |
| S25 | 3.6 mg · C/10 140 cyc 848 (83.2 %) | 참고 |
| S26 | DOL/DME 율별 곡선 (0.5C ≈625) | `Fig. 5b` 본문 숫자 대조용 |
| S27 | 45 °C CE — MSE ≈94–95.5 · 기준 ≈91.5 → ≈83.5 · CPME 최저 | CE < 95 % 를 '안정' 으로 쓰는 서술 감사 |
| S28 | 파우치 4.6 mg · E/S 4.5 · C/20 20 cyc 779 | 참고 |
| S29 | 30 cyc 뒤 Li SEM (배율 다름 10 대 20 µm) | 참고 |
| Table S1 | 용매 밀도 · 점도 · 유전율 (판매사 · 문헌) | 입력값 |
| Table S2 | 문헌 MSE/WSE 성능 비교 | 조건이 제각각인 비교표의 예 |
| Table S3 | 고전 MD 상자 분자 수 (TAME 행 'MtBE' 오기) | 고전 MD 조성 검산 입력 |

## 10. 비판 — 약한 곳 ★

**설계 · 대조군**

- ① **희석 교락**: MSE 는 1 M 염을 유지한 채 강용매 (DOL+DME) 를 70 % 로 줄였다 → 강용매당 염 1.43 배. CIP/AGG↑ · ¹⁹F 고자장 · LiF SEI · CE↑ 는 비용매 희석제나 염 농도만 올려도 같은 방향으로 나온다. '저밀도 · 비불소 공용매의 고유 효과' 를 보이려면 같은 비율의 비용매 희석제 대조군이나 1.43 M DOL/DME 대조군이 필요했다. 네 MSE 끼리의 차이는 작다 (CE 98.7–99.5 · i₀ 0.38–0.43 · 7Li −1.10 ~ −1.17).
- ② **'LiPS 용해 제한' 에 측정값이 없다**: 용해도 (적정 · UV-vis · S 정량) 가 논문 어디에도 없다. `Fig. 1c` · `Fig. S2` 는 0.5 M Li₂S₆/DOL 에 MtBE 를 **더 부은** 사진이라 1:1 이면 Li₂S₆ 0.25 M (1.5 M[S]) 로 희석된다 — 색이 옅어지는 것은 희석으로도 생긴다. 그리고 1:1 에서도 침전이 보이지 않는다. 즉 사진은 오히려 'DOL:MtBE 1:1 에 0.25 M Li₂S₆ 가 녹는다' 를 보여 준다. 실제 MSE 는 DOL+DME 70 % 라 용해도는 더 높을 것이다. 같은 CPME 를 쓴 shen2026 의 SSE (≈50–80 mM[S]) 와는 다른 체제다.
- ③ **`Fig. 1d,e` 결합에너지의 상태**: Li⁺ 1 개 + 리간드 1 개 착물을 IEFPCM 안에서 계산했고, MtBE · SBME · TAME 착물은 Li–O 2.55–2.57 Å 로 떨어져 있다 (DME · DOL · CPME 는 1.92–2.00 Å). 같은 단일 산소 에테르인데 거리가 0.6 Å 차이 나는 것은 극소 구조가 다른 상태 (입체 장애로 Li 가 옆에 걸린 꼴) 에 떨어졌을 가능성을 시사한다 — 배좌 탐색 · BSSE · PCM 용매 정체가 없어 '세 용매 ≈0.15 eV' 를 화학적 결합 세기로 못 읽는다. 식은 E_total − E_solvent − E_remain 인데 그림은 양수 (부호 반전 미기재).
- ④ **DFT 와 MD 의 순서가 엇갈린다**: CPME 는 DFT 로 Li⁺ 와 가장 세게 붙는데 (≈0.325 eV · MtBE 의 2 배) 고전 MD 첫 껍질 CN 은 가장 작다 (≈0.09 대 MtBE ≈0.18). 그리고 0.1 M Li₂S₆ ⁷Li 에서 CPME 만 고자장으로 간다. 논문은 이 불일치를 다루지 않는다 — 고전 MD 전하 축척 (용매 1.2 배 · 이온 0.8 배) 이 결과를 좌우했을 수 있다.
- ⑤ **'탈용매화 장벽을 낮춘다' (초록 · 결론)**: Li\|Li Ea 는 MtBE 만 0.7 kJ mol⁻¹ 낮고 CPME · SBME · TAME 은 기준보다 1.7–3.0 kJ mol⁻¹ **높다**. 점 6 개 · 셀 1 · 오차 없음. 저자 본문도 '비슷하다' 고 썼다 — 초록 · 결론의 표현이 본문보다 세다. Li₂S₆ 쪽 Ea (44.4 → 41.1) 도 오차 없이 3.3 kJ mol⁻¹ (34 meV) 이고, Rct 자체는 MSE 가 1.7–2.2 배 높다.
- ⑥ **β → α 귀속**: β-S₈ 는 실온에서 준안정이라 시간이 지나면 α-S₈ 로 간다. `Fig. S23` 은 DOL/DME 전극을 MSE 에 담근 것 하나뿐이고 DOL/DME 에 같은 시간 담근 대조 · 담금 시간 · 온도가 없다. operando 에서 MSE 셀이 충전 끝 ≈3–4 h 안에 α 로 간 것은 실제 관찰이지만, '용해–재석출을 바꾼 MSE 의 기전' 인지 'MSE 셀의 충전이 조금 길어 (≈17.4 h 대 ≈16.3 h · figure-read) 생긴 시간 효과' 인지 못 가른다.

**본문 수치 ↔ 자기 그림**

- ⑦ **율 숫자**: 본문 "C/2 에서 781 · 기준 700 → 10 cyc 뒤 < 550". `Fig. 5b` (600 dpi 확대) 의 C/2 구간은 MSE ≈712 → ≈690 · 기준 ≈630 → 545 이고, `Fig. 5c` 의 MSE C/2 방전은 ≈720 · `Fig. S26` 의 기준 C/2 는 ≈625. 781 · 700 은 **0.4C 구간 첫 값** (≈780 · ≈700) 에 맞는다 — 한 칸 밀려 적은 것으로 보인다. '< 550' 은 C/2 끝 값과 맞는다.
- ⑧ **45 °C 첫 CE**: 본문 MSE 79.7 % · `Fig. 5e` '1st cycle' 곡선은 방전 ≈1280 · 충전 ≈1430 mAh g⁻¹ (figure-read) → ≈89 %. `Fig. S27` 둘째 점 근처 MSE CE 가 ≈80 % 에 찍혀 있어 79.7 % 는 다른 화성 사이클 값일 수 있다 — CE 정의 (방전/충전 순서) · 어느 사이클인지 미기재.
- ⑨ **NMR 두 그림의 ⁷Li 화학 이동이 다르다**: 같은 0.1 M Li₂S₆ 용액인데 `Fig. 3a` 는 DOL/DME 0.17 · MtBE 0.28 ppm · `Fig. 3c` (DOSY) 는 ≈0.0 · ≈0.24 ppm. 기기가 셋 (Bruker 500 · Agilent 400 · Varian 600) 이고 어느 그림이 어느 기기인지 · 기준 보정이 같은지 미기재.
- ⑩ **정전위 석출 '정점 시간이 비슷'**: 0.266 대 0.234 h (12 % 빠름) · 정점 전류 1.5 배 · 용량 1.44 배. 실험 조건 (Li₂S₈ 농도 · 양 · 전극 · 사전 방전 · 배경) 이 Methods 에 없다.
- ⑪ **라벨 · 단위 오기 모음**: 초록 '4.5 µL mg s⁻¹' · `Fig. 2g` · `Fig. S12` '0.5 mA cm⁻¹' · `Fig. 3h` · `Fig. S20` x 축 'tau (Ω)' · `Fig. S3` Raman y 축 'Absorbance' · `Fig. S16` 캡션 'MST-MtBE' · `Table S3` TAME 행 '244 MtBE' · `Fig. 2d` 색 규약 불일치 · `Fig. S29` 두 SEM 배율 다름 (10 대 20 µm).

**측정 · 해석**

- ⑫ **XPS 깊이 등고선** (`Fig. 6c`): 색 막대에 숫자가 없다 — 지도마다 정규화했다면 '기준이 S²⁻ 가 훨씬 강하다' 같은 시료 사이 비교는 못 한다. 세척 · 공기 차단 이송 · 스퍼터 조건 미기재. 168.7 eV 'SO₄²⁻/─SO₂' 는 잔류 LiTFSI (─SO₂─) 와 겹친다 — 세척을 안 했으면 MSE 쪽 '산화 S 많음' 은 염 잔류일 수 있다.
- ⑬ **셔틀 '억제' 의 크기**: 45 °C 평균 CE 94.6 % 는 사이클마다 ≈5 % 전하가 셔틀 · 부반응으로 샌다는 뜻이다. 2.25 V 유지 전류 0.013 mA 도 ≈C/390 의 누설이다. '효과적 억제' 는 기준 대비 상대적 표현으로만 맞다. 셀 각 1 개 · 재현 셀 수 미기재 (전 성능 그림).
- ⑭ **DOSY 와 σ 의 엇갈림**: 염 없는 Li₂S₆ 용액에서 D(Li⁺) · D(DME) 가 MSE 에서 크지만, 실제 전해질 σ 는 MSE 가 39 % 낮다 (`Fig. S21`). 본문은 DOSY 로 "실제 셀에서 빠른 물질 이동" 을 말하는데, 실제 전해질에서 같은 측정은 하지 않았다 (TFSI⁻ 는 오히려 느려졌다).
- ⑮ **GITT-EIS 분해**: η_ohm 이 최대 2.8 mV 라 '무시 가능' 이라는데, 이 값이 σ (−39 %) 를 반영한 1.34 배다 — 수송 손해는 실재하고 단지 이 셀 조건 (E/S 10 · C/10) 에서 작을 뿐이다. η_act 는 MSE 가 핵생성점에서 2 배 (19.5 대 10.4 mV). 분극 이득은 방전 **끝** (84–92 % DOD) 의 η_conc 에서만 나온다 — '젖음' 사진 한 쌍이 그 근거다.
- ⑯ **파우치**: 양극 한 장 ≈24 cm² · 3.5 mg cm⁻² → 우리 산수 ≈65 mAh 급 (한 면 가정). Ah · Wh kg⁻¹ · 압력 · 장수 미기재. 4.6 mg · E/S 4.5 는 C/20 20 사이클뿐이다.
- ⑰ **`Table S2` 비교의 불공정**: 이 논문 코인 (E/S 10) 은 표의 다른 코인 (E/S 5–8) 보다 전해액이 넉넉하다. 온도 · 율 · 하중도 제각각이라 '고성능 MSE 와 비교' 는 서열을 주지 못한다.
- ⑱ **'저밀도' 의 이득**: 밀도 1.16 → 1.04 g cm⁻³ (−10 %) · 셀 수준 에너지 밀도 이득 계산은 없다. E/S 5.5 파우치에서 전해액 질량 이득은 ≈10 % 의 전해액 질량이다.

## 11. 적용 인사이트 ★ (우리 연구에 어떻게)

- ① **'희석 효과' 를 먼저 빼고 '고유 효과' 를 말한다** — 혼합물 · 도핑에서 조성을 바꾸면 여러 양이 동시에 바뀐다 (여기선 공용매 정체 + 강용매/염 비). 우리 도핑 · 혼합 계산에서도 '도펀트 효과' 를 말하기 전에 같은 셀 · 같은 화학량론 변화를 주는 대조 (예: 같은 공공 수 · 같은 Cl/S 비) 를 보고량 카드 단계에서 정해 둔다 — shen2026 (같은 σ 대조군 부재) 과 같은 교훈이 두 편 연속 나왔다.
- ② **결합에너지 1:1 착물의 '상태' 를 먼저 정의한다** — Li⁺ 1 + 리간드 1 은 실제 배위 상태가 아니고, 같은 계열 리간드에서 Li–O 거리가 0.6 Å 갈리면 서로 다른 극소에 떨어진 것이다. 우리 SDCP 마감 (`db/properties/sdcp_neutral_closed_2026_08_28.json`) 의 '상태 선택 규칙' 과 같은 규율이 이 외부 값에도 걸린다 (회신 N: 선택 · 집계 규칙 없으면 스칼라 미정의).
- ③ **방법이 다른 두 계산의 순서가 엇갈리면 그것부터 보고한다** — DFT (CPME 최강) ↔ 고전 MD (CPME 최약). 우리도 UMA MLIP 와 DFT 의 순위가 엇갈리면 (예: 자리 선호 · 결합 순서) 원고에서 숨기지 않고 '어느 방법의 무엇이 다른가' 를 적는다.
- ④ **겉보기 Arrhenius Ea 의 홉 수 검산** — Rct 기울기에서 낸 41 kJ mol⁻¹ 를 단일 장벽으로 놓으면 1/Γ ≈µs 인데 DRT τ 는 ms–0.1 s 다. 우리 규칙 (`D-2026-09-27-barrier-hop-count`) 이 '전기화학 겉보기 Ea' 를 '원자 장벽' 으로 잘못 옮기는 것을 막는 데도 쓸모가 있다 — 문헌 Ea 를 우리 NEB 장벽 옆에 놓기 전에 이 한 줄을 붙인다.
- ⑤ **본문–그림 대조 체크 (문헌 읽기)** — 율 표의 숫자는 한 칸 밀려 적히기 쉽다 (여기 781 = 0.4C). 율 성능 숫자를 인용할 땐 그림의 해당 구간을 직접 판독해 같이 적는다.
- ⑥ **전고체 Li–S 와의 다리** — 이 논문은 '액체 전해질을 덜 녹이게' 쪽이고, 같은 일을 전고체에서 하는 것은 용매가 없는 SE 자체다. 그 SE 가 충전 창에서 산화된다는 것 (우리 축 ① · `yu2025` · `cronk2026`) 이 전고체 쪽 문제다. 이 논문은 비교의 **액체 쪽 끝점**으로만 쓴다.
- ⛔ 하지 않는 것: 이 논문을 근거로 새 li2s 카드 · 트랙 · 런을 제안하지 않는다 (li2s 계열 2026-11-16 닫힘). 이 논문의 Li₂S · S₈ 관찰은 우리 SEI 트랙 Li₂S 결정 NEB 와 다른 질문이다.

## 12. 인용 가능 문장 (영문 초안 · 랩 표기 *Angew. Chem. Int. Ed.*, 65, e22940 (2026))

- "Replacing 30 vol% of the DOL/DME solvent with methyl tert-butyl ether (1 M LiTFSI, 0.2 M LiNO₃) raised the Li plating/stripping Coulombic efficiency from 98.0% to 99.5% and lowered the shuttle current at 2.25 V from 0.047 to 0.013 mA, while the ionic conductivity decreased from 11.68 to 7.11 mS cm⁻¹."
- "In that study, the activation energy of the Li|Li charge-transfer resistance changed by less than 1 kJ mol⁻¹ with the MtBE co-solvent and increased with the other three ether co-solvents, so the improvement was attributed to the pre-exponential factor rather than to a lower desolvation barrier."
- "Because the salt concentration was kept at 1 M while the strongly solvating solvents were reduced to 70 vol%, the reported increase in contact-ion pairing is not separated from a simple dilution of the solvating solvents."
- "Operando XRD showed β-S₈ followed by α-S₈ at the end of charge in the MtBE-containing electrolyte, whereas only β-S₈ appeared in DOL/DME; no time-matched immersion control in DOL/DME was reported."

## 13. 주의 / 한계 (인용 규율)

- **인용해도 되는 것 (조건을 붙여서)**: σ 11.68 → 7.11 mS cm⁻¹ · Li CE 98.0 → 99.5 % (Aurbach · 0.5 mA cm⁻² · 셀 1) · 셔틀 전류 0.047 → 0.013 mA (2.25 V · 3.5 mg cm⁻² · E/S 10) · 3.7 mg cm⁻² C/5 180 cyc 710 대 458 mAh g⁻¹ · 45 °C 90 cyc 799 대 627 · 평균 CE 94.6 대 89.4 % · 고전 MD CN(O_DME) ≈3.6 → ≈3.0 (figure-read · 단일 궤적).
- ⛔ **인용 금지**:
  - 'MSE 의 LiPS 용해도가 낮다' 를 수치처럼 (측정값 없음 · 사진은 희석과 섞임).
  - '탈용매화 장벽이 낮아졌다' 를 MSE 일반으로 (MtBE 만 −0.7 kJ mol⁻¹ · 나머지는 높음).
  - `Fig. 1d` Li⁺–용매 결합에너지를 용액 속 용매화 세기 순서로 (1:1 착물 · PCM · 세 착물 Li–O 2.55 Å).
  - `Fig. 2e` DME–용매 0.17–0.19 eV 차이를 '가장 강한 상호작용' 의 증거로 (0.02 eV · BSSE 없음).
  - 'C/2 에서 781 mAh g⁻¹' (그림은 ≈700–712).
  - 'β → α 두 단계 석출은 MSE 특유' 를 확정으로 (대조 담금 없음).
  - 파우치를 Ah 급 실용 셀로 (≈24 cm² 한 장 · 에너지 밀도 미보고).
- 액체 전해질 문헌이다 — 우리 SE 물성 (σ · Ea · ESW · 기계 · gap) 과 **같은 표에 놓지 않는다**. 이 논문의 'moderately solvating' 은 조작적 정의 (단일 산소 에테르 30 vol% 혼합) 이지 용해도 기준이 아니다 — SSE (< 100 mM[S]) 와 같은 범주로 옮기지 않는다.

## 14. 이어 읽기 — litdb 의 관련 digest

| digest | 이 논문과 닿는 곳 | 같이 읽을 때 |
|---|---|---|
| `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` | **같은 CPME** 를 다른 자리에 쓴 짝 — 저기선 CPME 가 주용매 (SSE · LiPS ≈50–80 mM[S]) 에 THF 를 조금 · 여기선 DOL/DME 가 주용매에 CPME 등 30 % | 두 편 다 '두 용매 상호작용' 을 0.2 eV 급 기상 이량체 하나로 받치고, 둘 다 결정적 대조군 (같은 σ · 같은 희석) 이 없다 · 둘 다 재충전 S 다형 (β-S₈) 을 다룬다. CPME 의 Li⁺ 결합 (여기 ≈0.325 eV) 과 shen2026 의 CPME 배위 서술을 나란히 보면 '약용매' 의 정의가 논문마다 다르다는 것이 보인다 |
| `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` | 준고체 Li–S · 전해질 용매화 + 매개자 | 용해도를 실제로 쟀는지 · 준고체 판정 기준 비교 |
| `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` | argyrodite 분리막 + 이온액체 준고체 Li–S · 고–액 계면상 | 액체 전해질 쪽 SEI 논리가 SE 가 낀 계면에서 어떻게 바뀌는지 |
| `guan2026_feco_vs_in2s3_li2s_electrocrystallization` | Li₂S 전기결정화 · 정전위 석출 | 이 논문 `Fig. S18` 은 Scharifker–Hills 맞춤조차 없는 정전위 석출 — 판정 감사 짝 |
| `wei2026_data_driven_hea_mediator_lis` | 액체 Li–S · GITT/DRT · 흡착 DFT 보고 규약 | DRT · 겉보기 Ea 를 읽는 방식 비교 |
| `luo2026_lis_separator_crystal_engineering_review` | 액체 Li–S 분리막 · '작동 상태 ≠ 초기 상태' | α-S₈ (초기) → β-S₈ (재충전) → α-S₈ (MSE) 가 그 구체 사례 |
| `lin2026_p_doped_compounds_li_s_review` | 액체 Li–S 양극 숙주 리뷰 | 전해질 쪽 전략은 범위 밖 — 이 논문이 그 빈자리 하나 |
| `yu2025_cng_host_suppress_argyrodite_oxidation_lis` | 전고체 Li–S 에서 argyrodite 산화 억제 (숙주 구조) | 액체에서 '용매가 덜 녹이게' 하는 일을 전고체에서는 '숙주가 SE 산화를 덜 일으키게' 로 한다 — 우리 축 ① 과 직접 닿는 쪽 |
| `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` | 전고체 Li–S 삼상 계면 · 혼합 전도체 · AIMD | 용매가 없으면 용매화 조절이 불가능 → 혼합 전도체가 대신한다 · AIMD 보고 항목 비교 |
| `cronk2026_lis_cathode_interphase_chemistry` | LPSCl 촉매전해질 · S 표면 Li₃PS₄₊ₙ · Li₂S 양극의 LPSCl 분해 | 전고체에서 '반응하는 전해질' 은 SE 자신 — 이 액체 논문의 XPS 산화 S 귀속과 대조 |
| `cronk2026_lis_positive_electrode_geometry_fem` | 전고체 Li–S 양극 기하 · 활성 표면 | 이 논문의 '젖음 → 방전 끝 η_conc↓' 는 그 FEM 의 활성 표면 개념의 액체판 |
| `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` | 전고체 Li–S 반응 기전 지도 | 액체 (이 논문) → 준고체 → 전고체 사다리 |
| `shang2026_uio66_anion_competition_peo_lis` | 고분자 전해질 Li–S · 음이온 경쟁으로 용매화 재구성 | '음이온을 Li⁺ 껍질로 들이는' 같은 목표의 고분자판 |
| `lee2026_eecfp_dnn_electrolyte_ce_lmb` | Li 금속 CE 예측 (전해질 설계 ML) | 이 논문의 CE 98.0–99.5 % 와 같은 측정 (Aurbach) 을 데이터로 쓰는 쪽 — CE 측정 프로토콜 차이 주의 |
| `ma2025_active_learning_electrolyte_solvent_screening_anodefree` | 전해질 용매 탐색 (능동 학습) | 이 논문의 '용매 넷 손으로 고르기' 와 대조되는 체계적 탐색 |

## 15. 기법 용어 미니사전

- **MSE (moderately solvating electrolyte)** — 강용매 (DME · DOL) 와 약한 용매를 섞어 Li⁺ · LiPS 용매화를 중간으로 맞춘 전해질. 이 논문에서는 단일 산소 에테르 30 vol% 혼합의 조작적 정의다.
- **WSE · SSE · LHCE** — 약용매화 전해질 · 폴리설파이드를 거의 안 녹이는 전해질 (< 100 mM[S] 를 흔히 기준) · 국소 고농도 전해질 (고농도 염 + 비용매 희석제).
- **SSIP · CIP · AGG** — 용매 분리 이온쌍 · 접촉 이온쌍 · 음이온 응집체 (TFSI⁻ S–N–S Raman 띠로 가름 · 이 논문은 CIP/AGG 를 한 성분으로 묶었다).
- **DOSY** — 확산 정렬 NMR. 봉우리마다 자기확산계수 D 를 준다 (분자 · 이온별 이동성).
- **ESP** — 정전기 전위 등면 (분자 표면의 전하 분포 그림).
- **IEFPCM** — 내재 (연속체) 용매 모형의 한 판. 분자 주위를 유전체로 둘러싸 용매 효과를 흉내 낸다 — 어떤 유전율을 썼는지가 결과를 바꾼다.
- **BSSE** — 유한 기저에서 짝 분자의 기저를 빌려 결합이 과대평가되는 오차 (counterpoise 로 보정).
- **CN (배위수)** — g(r) 첫 껍질 적분. 여기선 Li⁺ 주변 특정 산소 종의 개수.
- **SAXS** — 소각 X 선 산란. q ≈ 2π/d 로 수 Å–수십 nm 규모의 밀도 요동 · 군집을 본다.
- **Tafel · i₀** — 과전압–log 전류 직선에서 교환전류밀도 (전극 반응의 고유 속도) 를 낸다.
- **DRT** — 임피던스를 시간 상수 분포로 풀어 봉우리마다 저항을 준다 (봉우리 면적 = 저항).
- **Aurbach CE** — Li 저장량을 깔고 짧은 증착–박리를 반복한 뒤 남은 Li 를 벗겨 평균 쿨롱 효율을 내는 법.
- **GITT-EIS 분극 분해** — 전류 계단의 순간 점프 (옴 + 활성화) · 고주파 절편 (옴) · 휴지 중 표류 (농도) 로 과전압을 셋으로 나눈다.
- **셔틀 전류** — 일정 전압 유지 중 녹은 LiPS 가 양극–음극을 오가며 흘리는 누설 전류.
- **α-S₈ · β-S₈** — 사방정 (실온 안정) · 단사정 (95.3 °C 위 안정 · 실온 준안정) 황. Li–S 재충전에서 β 가 먼저 나오는 보고가 많다.
- **E/S · DOD · SOC** — 전해액 (µL) / 황 (mg) · 방전 깊이 · 충전 상태 (%).
- **S 2p 귀속 (이 논문)** — SO₄²⁻/─SO₂ 168.7 · SO₃²⁻/─SO 167.1 · S⁰ 원소 164.5 · S_B⁰ (다리 S) 163.6 · S_T⁻¹ (끝 S) 161.6 · S²⁻ 159.9 eV (각 2p₃/₂).
- **관측창 · 홉 수 검산** — 우리 규칙 두 개: 짧은 MD 에서 '없다' 를 말할 때 기대 사건 1 의 장벽 (Ea₁ = kT ln(ν₀ t n)) 을, 장벽을 인용할 때 Γ = ν₀ exp(−Ea/kT) 를 같이 적는다 (ν₀ 10¹³ s⁻¹ 가정).

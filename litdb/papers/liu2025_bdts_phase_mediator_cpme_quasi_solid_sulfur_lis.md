<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 기준 = papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md
     2026-11-26 신규 — 논문 에이전트 (API 배치 · inbox '9.' 묶음). 본문 13 pp + SI 48 pp 글자층 전문 정독 · 그림 크롭을 Read 로 직접 봤다 (§0 목록).
     그림 폴더 손질: extract_figures.py 가 ① 본문 그림 6 장을 오른쪽 절반에서 잘랐고 (전폭 그림) → 페이지 그래픽 범위로 다시 자름 (recrop) ·
       ② Extended Data Fig. 1 을 'S1' 로 붙여 진짜 Supplementary Fig. 1 과 부딪쳤다 → ED1 로 바꾸고 S1 을 손으로 자름 ·
       ③ SI 벡터 그림 S2 · S4 · S8 · S13 · S15 · S18 을 놓쳤다 → 손 크롭 (manual_crop) · ④ 표 S1 · S2 · S4 를 목차 쪽에서 잘랐다 → 표 쪽에서 다시 자름.
     ⛔ 그림 폴더를 `extract_figures.py --clean` 으로 다시 돌리지 않는다 — 손 크롭 · recrop 이 지워진다.
     talk 인입 대기열: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → lee2026_skku_mlip_materials_design.md 하나 · 이 논문 행 없음 (확인).
     ⚠ 이 논문은 **액체 (약용매화) 전해질 Li–S 전지** 논문이다 — argyrodite SE 물성 4축 (A–D) 에 행을 만들지 않는다.
       쓰는 곳은 방법 (AIMD 용매화 통계 · 고전 MD 대조 · QE-Environ 연속 용매화 · 분자 클러스터 결합에너지) · 개념 (준고체 황 반응 · 표면 국소 용매화 · 상 매개자) · 보고 규약 감사.
     영상 2 편 (Supplementary Video 1 · 2 = AIMD 궤적) 과 Source Data zip 은 보지 않았다 · 열지 않았다. -->

# Surface-localized phase mediation accelerates quasi-solid-state reaction kinetics in sulfur batteries — Liu, An et al. (*Nat. Chem.* 17, 614–623 (2025))

> slug `liu2025_bdts_phase_mediator_cpme_quasi_solid_sulfur_lis` · DOI `10.1038/s41557-025-01735-w` · type `mixed — exp 주 (Raman · ⁷Li NMR · UV–vis · GITT · CV · LSV/Tafel · EIS · operando XRD · operando S K-edge XANES · SEM · XPS · 점도 · 코인/파우치) + 계산 보조 (VASP 계열 PAW-PBE-D3 AIMD 6 런 · LAMMPS OPLS 고전 MD 5 계 · QE 7.2 + Environ SCCS 연속 용매화 2 클러스터 · B3LYP-D3(BJ)/6-31+G(d,p) IEFPCM 클러스터 결합에너지 · LUMO · Mulliken — NEB 0 · MLIP 0 · 슬랩 0 · DOS/Bader/COHP 0)` · PDF `litdb/inbox/9. Surface-localized phase mediation accelerates quasi-solid-state reaction kinetics in sulfur batteries.pdf` (본문 13 pp · Methods · Extended Data Fig. 1) + `9. Sup) … .pdf` (SI 48 pp · Supplementary Fig. 1–24 · Table 1–9 · Note 1–2) · 영상 2 (`9. Sup2)` · `9. Sup3)` .mpg — 안 봄) · Source Data zip (`9. Sup4)` — 안 엶) · digested `2026-11-26` · status ✅ · 태그 **[외부 · 액체 전해질 Li–S (약용매화) · 비-argyrodite]**
> elements: Li, S, C, N, O, F
> methods: DFT, AIMD, MD, XPS, Raman

> **저자**: **Yatao Liu** (1저자 · 北京大学 + 北京化工大学) · Yun An · Chi Fang · Yaokun Ye · Yifeng An · Mengxue He · Yongfeng Jia · Xufeng Hong · Yumei Liu · Song Gao · Yizhou Hao · Jianhao Chen · Jiaxin Zheng · Yunfeng Lu · **Ruqiang Zou\*** · **Quanquan Pang\*** — 北京大学 材料科学与工程学院 (Beijing Key Laboratory for Theory and Technology of Advanced Battery Materials) · 北京化工大学 (State Key Laboratory of Organic–Inorganic Composites · Beijing Advanced Innovation Center for Soft Matter) · 北京大学 深圳研究生院 新材料学院 · 北京大学 物理学院 量子材料中心. 교신 rzou@pku.edu.cn · qqpang@pku.edu.cn.
> 접수 2024-02-02 · 수락 2025-01-06 · 온라인 2025-02-13 · *Nat. Chem.* 17 권 (2025 년 4 월) 614–623. 자금: NSFC 92372115 · 22075002 · 52203347 · 51825201 · 52227802 · 22409006 · 国家重点研发 2021YFB2500200 · 北京市自然科学基金 Z220020 · 中国博士后 2021M690001 · 中国石油–北大 전략협력. XANES = BSRF 4B7A. 심사자: Nav Nidhi Rajput · Sebastian Risse 외 익명. 이해 상충 없음.
> 기여 진술 (계산 담당이 적혀 있다): **AIMD = Yun An** · **DFT = Yun An · Y. Ye** · **고전 MD = C. Fang · Y. Ye · J. Zheng**. 실험 = Yatao Liu.
> **계보**: Lee 2017 *ACS Cent. Sci.* (SSE 반응 경로 · ref 24) → Pang 2018 *Nat. Energy* (전해질 망 구조로 준고체 전환 · ref 22) → Liu 2021 *Joule* (Li–S 전해액 설계 리뷰 · ref 32) → Liu 2023 *Joule* (반용매로 길들인 QSSSR · ref 23) → **본 논문** (약용매화 CPME + 분자 '상 매개자' BDTS) → 같은 그룹의 후속: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` (매개자 분자 대신 THF 공용매) · `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` (실록산 약용매화 + DIP 매개자 · 교신 Yatao Liu).
> 🔗 **이어 읽기 (litdb Li–S)**: 같은 그룹 — `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` · `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` / 같은 CPME 계열 · 용매 지도 — `lai2026_mtbe_moderately_solvating_ether_cosolvent_lis` · `peng2026_er_dn_solvent_screening_csa_methf_lis` / 매개 · 핵생성 — `wei2026_data_driven_hea_mediator_lis` · `guan2026_feco_vs_in2s3_li2s_electrocrystallization` / 준고체 · argyrodite 다리 — `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` · `yu2025_cng_host_suppress_argyrodite_oxidation_lis` / 전고체 Li–S — `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` · `cronk2026_lis_cathode_interphase_chemistry` · `cronk2026_lis_positive_electrode_geometry_fem` · `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` — 대응은 §14.

---

## 0. 이 digest 를 읽는 법

**읽기축 (우리 트랙에서의 자리)**: 황화물 SE 가 아니라 **액체 전해질** (1 M LiTFSI in CPME + 50 mM BDTS) Li–S 전지 논문이다. 가져올 것은 셋 — ① **계산 방법 대조** (AIMD 용매화 통계를 Li⁺ 2 개로 낸 사례 · 고전 MD 와 AIMD 의 CN 불일치를 다루는 방식 · QE-Environ 연속 용매화 에너지의 쓰임새와 한계 · 분자 클러스터 결합에너지의 기준 상태), ② **개념** (준고체 황 반응 QSSSR · '표면 국소 용매화' · 상 매개자 vs 산화환원 매개자 · 재충전 황의 다형 α/β/γ-S₈), ③ **보고 규약 반례** (율 성능 비교가 **서로 다른 방전 하한 전압**에서 이뤄졌다 · 그림 캡션과 패널 라벨이 엇갈린다 — §10).

**판정 요약 (§6 · §10 상세)**:

| 주장 | 판정 | 핵심 근거 |
|---|---|---|
| 1 M LiTFSI–CPME 는 약용매화 전해질이다 (CIP 지배 · Li₂S₆ ≈8 mM[S]) | ✅ 방향은 받친다 | Raman 띠 ≈747 cm⁻¹ = 고체 LiTFSI 와 같은 자리 (`Fig. 2a`) · ⁷Li NMR 저자장 이동 · 용해도 (측정법은 '포화까지 넣기' 뿐) |
| CPME 계에는 드문 **3 배위 Li⁺** 가 55 % 있다 (AIMD) | ⚠ 한 상자 **Li⁺ 2 개** · 생산 구간 미기재 · 시작 구조를 바꾸면 **종별 CN 분배가 뒤바뀐다** (`Fig. S2a` CPME 2.0/TFSI 1.4 ↔ `Fig. S2d` CPME 1.4/TFSI 2.0) · 고전 MD 는 3 배위 7.5 % · 4 배위 81 % | §5.2 · 관측창 ≈0.14 eV |
| 연속 용매화 DFT 가 3·4 배위의 '열역학적 존재' 를 확인한다 | 🔴 근거가 안 된다 — 극성 용질의 ΔG_sol 은 거의 늘 음수 · 저자 스스로 "구조 간 비교에 못 쓴다" 고 적었다 · 단위 환산이 두 배 어긋난다 (Ry ↔ kcal) | §5.3 |
| BDTS 환원체 (BDTSRed) 가 Li₂S₆ 와 착물을 만들어 녹인다 (≈150 mM Li₂S₆ · 1:3) | ✅ 사진 · UV–vis 로 받친다 · ⚠ BDTS ↔ BDTSRed UV–vis 가 거의 같아 '환원체' 의 정체 (C–S 절단) 는 분광 증거가 없다 | `Fig. S9a,c` |
| 용해는 '**표면에 국소화**' 된다 | 🔴 공간 국소화를 잰 실험이 없다 — 대신 벌크 용해도가 ≈8 → ≈900 mM[S] (우리 환산) 로 ≈110 배 오른다 · 첫 평탄의 S₈ 소비 속도가 DME (캐솔라이트) 와 같다 (`Fig. 5c`) | §6 |
| 상 매개는 고전적 산화환원 매개 (RM) 와 다르다 | ⚠ LiI 한 분자와 비교했을 뿐 — BDTS 자신이 2.42/2.20 V 환원 · 2.66 V 산화하는 산화환원 활성 분자라 RM 경로를 배제하지 못한다 | §6 · §10-④ |
| 16 C 494 · 10 C 583 mAh g⁻¹ · 촉매 캐솔라이트보다 율 성능이 낫다 | 🔴 **방전 하한 전압이 다르다** — BDTS 셀 10 C 는 30 °C 에서 ≈0.5 V · 55 °C `Fig. S19f` 에서 ≈0.2 V 까지 · 비교 DOL/DME 셀은 1.5–1.7 V (`Fig. S19e`) · 충전도 4.0 V 까지 | §5.8 · §10-① |
| 300 cyc 90 % · 200 cyc 95 % · 2 C 300 cyc 안정 | ⚠ 기준 사이클 미기재 — `Fig. 6f` 는 첫 ≈1200 → ≈15 cyc 에 ≈810 으로 떨어진 뒤의 '안정' (figure-read) | §5.8 |
| 희박 전해액 · 고부하 장기 사이클 | ⚠ **방전 용량 고정 (800 mAh g⁻¹ · 3.75 mAh cm⁻²) · 55 °C** — 캡션에 밝혔다 (정직) · 고정 없이 1.9–3 V 는 `Fig. S22` | Extended Data Fig. 1a–c |
| 2.4 Ah · 331 Wh kg⁻¹ 파우치 24 cyc '안정' | ⚠ 40 °C · 24 cyc 에 figure-read ≈2350 → ≈1630 mAh (≈69 %) · CE ≈93–97 % | Extended Data Fig. 1d |

**본 digest 에서 실제로 본 그림 (2026-11-26)** — 크롭 40 장 (본문 그림 6 + Extended Data 1 + SI 그림 24 + SI 표 9) 중:

- 원해상도로 본 것 **15 장**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` · Extended Data Fig. 1 (`fig_ED1.png`) · `Fig. S2` · `Fig. S3` · `Fig. S9` · `Fig. S12` · `Fig. S13` · `Fig. S14` · `Fig. S17` · `Fig. S19`.
- **안 본 것 (글자층만 읽음)**: `Fig. S1` (Raman 맞춤 · LiTFSI 결정 · DME 착물) · `Fig. S4` (고전 MD) · `Fig. S5` (점도 · THF 농후 AIMD) · `Fig. S6` (Li\|Cu · XPS · EIS) · `Fig. S7` (BDTS CV · dQ/dV) · `Fig. S8` (BDTS 단독 율 · 사이클) · `Fig. S10` (Mulliken) · `Fig. S11` (공명형 · Li₂S₄ 착물) · `Fig. S15` (LiI) · `Fig. S16` (다른 SSE) · `Fig. S18` (XANES) · `Fig. S20` · `Fig. S21` · `Fig. S22` · `Fig. S23` · `Fig. S24` — 이들 그림의 수치는 SI 본문에 인쇄된 값만 옮겼다 (figure-read 없음). 표 9 장 (`Table S1`–`S9`) 은 PDF 글자층으로 읽었다 (`Table S2` 는 숫자 열이 글자층에서 빠져 **값을 옮기지 못했다**).
- 그림에서만 읽은 값은 **`figure-read ≈`** 로 적었다. 판독 정밀도는 눈금 간격의 ≈ ±2–5 %.

---

## 1. 한 줄 요약

약용매화 에테르 **CPME** 에 1 M LiTFSI 만 녹인 저밀도 · 저농도 전해질이 TFSI⁻ 접촉 이온쌍 지배 용매화로 Li₂S₆ 용해도를 ≈8 mM[S] 로 누르고 Li 금속도 안정시키는데 (Li\|Cu 평균 CE ≈98.4 %), 그 대가인 느린 '준고체 황 반응 (QSSSR)' 을 **50 mM BDTS (bis(dimethylthiocarbamyl) sulfide)** 첨가로 가속한다 — 첫 방전에서 환원된 BDTS (BDTSRed, 디티오카르바메이트 계열) 가 Li₂Sₓ 의 Li⁺ 와 착물을 만들어 입자 **표면에서만** 폴리설파이드를 용액상으로 끌어내고, Li₂S · S₈ 가 되면 풀려나 다음 순환에 쓰인다는 '상 매개 (phase mediation)' 그림이다. 결과로 율 성능 (30 °C 10 C 583 · 55 °C 16 C 494 mAh g⁻¹) · 사이클 (0.2/0.1 C 300 cyc 90 %) · 2.4 Ah 331 Wh kg⁻¹ 파우치를 보고한다. 전해질 · Li 쪽 근거와 '용해도가 오른다' 는 관측은 받쳐지지만, **'표면 국소' 는 측정되지 않았고**, 율 성능 우위는 **방전 하한 전압 차이** (BDTS 셀 0.2–0.5 V vs 비교 셀 1.0–1.7 V) 를 걷어 내면 크게 줄어든다.

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | 1 M LiTFSI in CPME (`LiTFSI–CPME`, 기본 WSE) · + 50 mM BDTS (`BDTS–LiTFSI–CPME`) · 대조: 1 M LiTFSI in DME · 1 M LiTFSI + 2 wt% LiNO₃ in DOL/DME (1:1 v/v) · LHCE ((MTHF)₂–LiTFSI + 50 vol% HFE · 또는 TTE) · (THF)₂/(THF)₃–LiTFSI 농후 계 · LiI 20/50 mM (RM 대조) |
| 양극 | S/KB (70 wt% S · 155 °C 12 h 용융 확산) : Super P : PVDF = 8:1:1 · 탄소 코팅 Al · 기본 E/S **10 µL mg⁻¹** · 30 °C (Methods) · 미세 Li₂S 양극 (`Fig. S14a`) · BDTS 단독 (탄소종이 · `Fig. 4a` · `Fig. S7` · `Fig. S8`) · 파우치 S/그래핀 (75 wt% S) |
| 음극 | Li 금속 (파우치 125 µm · N/P ≈1.87) |
| 질문 | 약용매화 전해질 (SSE) 은 LiPS 용해를 막아 전극 반응을 전해액 부피에서 떼어 낼 수 있지만, 반응이 고체–고체가 되어 **느리고** (보고 율 0.05–0.2 C) 절연성 LiPS/Li₂S 가 표면을 막는다. **벌크 용해는 막으면서 반응 앞면에서만 용매화를 켤 수 있나?** |
| 답 (저자) | 낮은 농도에서 SSE 를 만드는 용매로 CPME (ε 4.76 · 사이클로펜틸 입체 장애) 를 고르고, LiPS 의 Li⁺ 를 S 로 붙잡는 BDTSRed 를 '상 매개자' 로 넣는다 — 착물이 표면 근처에 국소 용액 영역을 만들고, Li₂S · S₈ 와는 안 붙어서 (`Fig. S9e,f`) 순환이 닫힌다 (`Fig. 1c`) |
| 저자가 내세운 CPME 의 장점 | 저밀도 (본문 '0.984 g cm⁻³' — 아래 ⚠) · 끓는점 106 °C (DOL 75 · DME 85 °C) · 1 M 저농도 → 점도 **1.24 mPa s** (`Fig. S5a`) · 값 싸다 (`Table S5` · 전해액 1 M LiTFSI + 0.9 wt% BDTS) |
| ⚠ 밀도 숫자 | 본문은 "CPME has a low density of 0.984 g cm⁻³" — CPME 순용매의 문헌 밀도는 ≈0.86 g cm⁻³ 다 (**외부 지식 · 이 논문에 없는 값**). 0.984 는 1 M LiTFSI–CPME **전해액** 값일 가능성이 크다 (우리 AIMD 상자 역산 ≈0.96 g cm⁻³ · §5.2) |
| 연구 유형 | 실험 주 · 계산 보조 (계산은 용매화 구조 `Fig. 2c–g` · `Fig. S2–S5` · BDTS 환원/착물 `Fig. 4c,d` · `Fig. S10` · `Fig. S11`) |
| 우리와의 거리 | 황화물 SE 물성 4축 (A 이온 · B 산화 · C 기계 · D 전자) 수치 비교 없음. 방법 · 개념 · 보고 규약 쪽만 닿는다 (§7) |

## 3. 핵심 수치 총정리 ★

> 규율: 아래는 전부 **문헌 소환값**이다 — 우리 db 절대값과 한 표에 섞지 않는다. 본문 명시값과 `figure-read ≈` 를 칸마다 구분했다. 온도는 따로 적지 않으면 30 °C (Methods 기본).

### 3a. 전해질 구조 · 수송 (실험)

| 물성 | LiTFSI–CPME | LiTFSI–DME | 출처 · 비고 |
|---|---|---|---|
| TFSI⁻ S–N–S Raman 띠 중심 | figure-read ≈747 cm⁻¹ (고체 LiTFSI ≈747 와 같음) | figure-read ≈741 cm⁻¹ | `Fig. 2a` |
| Raman 맞춤 분율 | SSIP 0 · 단자리 CIP **31.6 %** · 두자리 CIP **68.4 %** | SSIP **50.0 %** · 단자리 CIP **41.0 %** · 두자리 CIP **9.0 %** | `Fig. S1a,b` (안 봄 · SI 본문 값) — SI 본문은 띠 위치를 "~740 nm · ~743 nm · ~748 nm" 로 적었다 (단위 오기 · cm⁻¹) |
| ⁷Li NMR 화학 이동 | figure-read ≈ −0.79 ppm · FWHM **2.156 Hz** | figure-read ≈ −1.16 ppm · FWHM **1.206 Hz** | `Fig. 2b` · 외부 기준 0.1 M LiCl/D₂O |
| Li₂S₆ 용해도 | **≈8 mM[S]** | **> 6 M** (ref 32 인용) | 본문 · 측정법 = "포화될 때까지 고체 Li₂S₆ 를 넣는다" (정량법 미기재) |
| Li₂S₆ 용해도 + 50 mM BDTSRed | **≈150 mM** (Li₂S₆ 기준 · BDTSRed : Li₂S₆ = 1:3) | — | 본문 · `Fig. S9b` 사진 — 우리 환산: ≈900 mM[S] (≈110 배) |
| S₈ 용해 + BDTSRed | ≈6 mM ("trace") · BDTSRed:S₈ 8:1 에서 미량 | — | 본문 · SI |
| 점도 (25 °C) | **1.24 mPa s** · DOL/DME+LiNO₃ 와 "매우 가깝다" | — | 본문 · `Fig. S5a` (안 봄) |
| Li\|Cu 평균 CE (0.5 mA cm⁻² · 2 mAh cm⁻²) | **≈98.4 %** | **≈66.7 %** (본문) / **66.3 %** (`Fig. S6a` 인쇄) | 본문 ↔ SI 가 0.4 %p 다르다 · SI 본문은 "< 80 %" |
| Li\|Li 600 h | 단락 없음 · 과전압 figure-read ≈0.08 → ≈0.15 V 로 **늘어난다** | figure-read ≈0.02–0.03 V → 300 h 뒤 출렁임 ≈0.07 V | `Fig. 3e` — 저자는 CPME 쪽을 "steady" 라 했다 (§10-⑨) |
| Li\|Li 70 일 휴지 뒤 계면 저항 R2 증가 | **+6.7 %** | **+104 %** | `Fig. S6l` (안 봄 · SI 본문 값) · CPME 쪽 R2 절대값이 더 크다 (SI 본문 인정) |

### 3b. 계산 (전부 문헌 소환값 · 방법은 §4e · §8)

| 양 | 값 | 출처 | 비고 |
|---|---|---|---|
| AIMD 평균 Li–O CN · 1 M CPME (고체 LiTFSI 꼴 시작) | **3.43** = O(CPME) **1.98** + O(TFSI) **1.45** | `Fig. 2c` · `Fig. S2a,f` | 절단 반경 figure-read ≈2.9 Å (점선) · g(r) 봉우리 figure-read ≈2.0 Å · 높이 TFSI ≈35 · CPME ≈26 |
| 같은 계 · 4 배위 시작 (**400 K**) | **3.46** · 3 배위 53.8 % · 4 배위 46.2 % | `Fig. S2d,f` | ⚠ 종별 CN figure-read: O(CPME) ≈1.4 · O(TFSI) ≈2.0 — (a) 와 **분배가 뒤바뀌었다** |
| 같은 계 · Li/TFSI 떼어 놓고 시작 | **3.44** · 2 배위 0.3 % · 3 배위 55.3 % · 4 배위 44.4 % | `Fig. S2e,f` | 종별 figure-read: O(CPME) ≈1.9 · O(TFSI) ≈1.4 |
| 2 M CPME | **3.63** · 2/3/4/5 배위 0.6 / 40.4 / 54.0 / 5.0 % | `Fig. S2b,f` | 종별 figure-read O(CPME) ≈1.0 · O(TFSI) ≈2.5 |
| 3 M CPME | **3.76** · 3/4/5 배위 38.4 / 47.0 / 14.6 % | `Fig. S2c,f` | — |
| 1 M DME | **4.62** = O(DME) **3.00** + O(TFSI) **1.62** · 4/5/6 배위 41.2 / 58.0 / 0.8 % | `Fig. 2d,e` · `Fig. S2f` | 절단 반경 figure-read ≈3.3 Å — **CPME 계 (≈2.9 Å) 와 다르다** |
| 1 M CPME 배위 분포 (AIMD a) | 2/3/4 배위 **1.2 / 55.2 / 43.6 %** | `Fig. 2e` | 산수 검산 (우리): 0.012·2 + 0.552·3 + 0.436·4 = 3.42 ≈ 3.43 ✓ |
| 상자 조성 (Methods + **우리 산수**) | 1 M = CPME 18 + LiTFSI 2 (374 원자 · 16³ Å³) · 2 M = 18 + 4 (406 · 16.5³) · 3 M = 18 + 6 (438 · 17³ — Methods 는 '17 Å for **2 M**' 오기) · DME = 18 + 2 (320 · 15³) | Methods ("9:1 · 9:2 · 9:3 by mole") | 원자 수: CPME C₆H₁₂O 19 · DME C₄H₁₀O₂ 16 · LiTFSI 16 → 9·19+16 = 187 × 2 = 374 ✓ 등 전부 맞는다. **Li⁺ 는 1 M · DME 상자에 2 개** |
| 상자에서 나오는 실제 농도 · 밀도 (**우리 산수**) | 1 M → **0.81 M** · ≈0.96 g cm⁻³ / 2 M → **1.48 M** · ≈1.09 / 3 M → **2.03 M** · ≈1.19 / DME → 0.98 M · ≈1.08 | 상자 부피 · 분자량 | 라벨 '2 M · 3 M' 은 몰비 (9:2 · 9:3) 의 이름이지 상자 농도가 아니다 |
| 고전 MD 평균 CN | CPME 0.25 M **4.00** · 1 M **4.07** · 2 M **4.24** · 3 M **4.27** · DME 1 M **5.65** | `Fig. S4` (안 봄 · SI 본문 · 표 글자층) | CPME 1 M 3/4/5 배위 7.5 / 81.0 / 11.5 % · O(CPME) 3.4 → 2.0 · O(TFSI) 0.6 → 2.3 (0.5 → 3 M) · ⚠ Methods 는 '0.25 M' · 그림 라벨은 '0.5 M' |
| 고전 MD 상자 (SI Methods) | 0.25 / 1 / 2 / 3 M = 3500 / 3740 / 4060 / 4380 원자 · DME 3200 원자 | SI Methods | 우리 산수: 1 M = CPME 180 + LiTFSI 20 (Li⁺ **20 개**) · 상자 농도 ≈0.84 M |
| 연속 용매화 ΔG_sol (QE-Environ · ε 4.76) | 4 배위 클러스터 **−0.0453 Ry (−28.4814 kcal/mol)** · 3 배위 **−0.0188 Ry (−11.8546 kcal/mol)** | `Fig. S3` · SI 본문 | ⚠ 1 Ry = 313.75 kcal/mol 이면 −0.0453 Ry = **−14.2 kcal/mol** — 적힌 kcal 값은 **Hartree 로 환산한 값** (0.0453 Ha = 28.4 kcal/mol). 둘 중 하나가 틀렸다 (§10-⑥) |
| BDTSRed–Li₂S₆ 결합에너지 (B3LYP-D3(BJ) · IEFPCM) | I figure-read ≈ −1.9 · I′ ≈ −2.1 · II ≈ −1.7 · II′ ≈ −2.45 eV | `Fig. 4d` | 본문에 숫자 없음 · E_b = E_total − E_BDTSRed − E_Li₂Sₓ (Methods) · BDTSRed 는 Li 가 붙은 꼴로 그려져 있다 |
| BDTSRed–Li₂S₄ · BDTSRed I (meso)–Li₂S₆ | 숫자는 `Fig. S11b,c` 그림에만 (안 봄) | `Fig. S11` | — |

### 3c. 동역학 · 상 변화

| 측정 | LiTFSI–CPME | BDTS–LiTFSI–CPME | LiTFSI–DME | 출처 · 비고 |
|---|---|---|---|---|
| GITT 방전 모양 | 준이중 평탄 ≈2.2 V | 준이중 평탄 2.2 V · ≈400 mAh g⁻¹ 에 전압 골 | 두 평탄 2.3 / 2.1 V + 충전 셔틀 (> 1700 mAh g⁻¹ 까지 계속) | `Fig. 3a` · `Fig. S12a` |
| BDTS 산화환원 (CV 0.1 mV s⁻¹ · BDTS 단독) | — | 활성화 1.439 V (첫 사이클) · 환원 2.416 · 2.196 V · 산화 2.659 V (+ 2.738 V) | — | `Fig. S7c` (안 봄 · 인쇄 값) — S₈ (CPME): 환원 2.132 · 1.820 V · 산화 2.494 V |
| S₈ 셀의 BDTS 환원 평탄 (2 번째 사이클) | — | figure-read ≈2.45–2.5 V · ≈50–60 mAh g⁻¹(S) | — | `Fig. S12b` · `Fig. 4e` — 1 번째 사이클 곡선에는 이 평탄이 거의 없다 |
| Tafel 교환 전류 밀도 j₀ (S₈ LSV) | **2.2 × 10⁻² mA cm⁻²** | **4.6 × 10⁻² mA cm⁻²** | — | `Fig. S13b` · 맞춤 구간 과전압 **0.080–0.090 V 단 10 mV** · 기울기 figure-read ≈125 / ≈110 mV dec⁻¹ (우리 검산으로 j₀ 재현됨 · §5.6) |
| BDTSRed + Li₂S₆ '반응 속도' | — | **1.38 × 10⁻⁵ mol L⁻¹ s⁻¹** (30 °C) | — | `Fig. S13` 논의 · 1 mL 50 mM BDTSRed + 10.3 mg Li₂S₆ (우리 산수: 0.050 mmol = 50 mM) · 끝점 = 육안 '완전히 맑아짐' → **≈3600 s ≈ 1 h** (우리 산수) |
| 미세 Li₂S 첫 충전 장벽 | **≈3.72 V** | **≈3.23 V** | — | `Fig. S14a` · BDTS 셀은 앞에 ≈2.5 V 계단 (BDTSRed 산화 · figure-read ≈40–50 mAh g⁻¹(Li₂S)) |
| EIS (반 방전) R1 / R2 / R3 | figure-read ≈28 / ≈130 / ≈172 Ω | ≈28 / ≈53 / ≈151 Ω | — | `Fig. S14c` · 셀 1 개씩 · 줄어든 것은 주로 R2 ('SEI') · 전하이동 R3 는 ≈12 % |
| 첫 충전 개시 장벽 (S₈ 셀 · 0.1 C) | figure-read ≈2.40 V | figure-read ≈2.30 V | — | `Fig. 4e` 삽입 |
| operando XRD — 20 % DOD 의 S₈ 남은 양 | figure-read ≈93 % (≈25 % DOD 까지 거의 그대로 → ≈28 % 에서 0) | figure-read ≈15 % | figure-read ≈20 % | `Fig. 5c` · 본문 "BDTS ~90 % 소비 at ~20 % DOD · DME 와 같은 수준" |
| 결정 Li₂S 첫 출현 | figure-read ≈47 % DOD | figure-read ≈51 % DOD | figure-read ≈35 % DOD | `Fig. 5c` |
| 충전 중 S₈ 재출현 | figure-read ≈92 % SOC | **≈58 % SOC** (본문 60 %) | figure-read ≈85 % SOC | `Fig. 5c` — BDTS 셀은 S₈ 가 다시 보일 때 Li₂S 가 아직 ≈30 % 남아 있다 (figure-read) |
| 충전 중 Li₂S 소멸 | figure-read ≈91 % SOC | figure-read ≈88 % SOC | figure-read ≈74 % SOC | `Fig. 5c` |
| 재충전 황의 상 | **γ-S₈** (단사정) | **α-S₈** (사방정 · 처음 양극과 같은 상) | **β-S₈** (단사정) | `Fig. 5d` · `Fig. S17a` · `Table S1` |
| 방전 끝 Li₂S 결정자 크기 (111) | **≈13.3 nm** | **≈11.8 nm** | **≈10.8 nm** | 본문 · `Fig. S17e` — 오차막대는 **같은 셀의 마지막 XRD 5 장** (독립 셀 아님) |
| S K-edge XANES (BDTS 셀) | — | 방전 350 mAh g⁻¹ 에서 LiPS 전가장자리 ≈2470.7 eV · Li₂S ≈2476.2 eV | — | `Fig. S18` (안 봄 · SI 본문) · S–S/S–C ≈2472.3 · TFSI⁻ ≈2480.2 · 2485.3 eV |

### 3d. 셀 성능

| 조건 | LiTFSI–CPME | BDTS–LiTFSI–CPME | 비교 셀 | 출처 · 비고 |
|---|---|---|---|---|
| 0.2/0.1 C · 100 cyc (`Fig. 3b`) | 첫 figure-read ≈1040 → ≈925 (≈89 %) · CE 99.8 % (본문) | — | DME ≈840 → ≈460 · DOL/DME+LiNO₃ ≈910 → ≈610 · LHCE ≈1030 → ≈490 (50 cyc 뒤 급락) | 본문 "~90 % retention" |
| 0.2/0.1 C · 300 cyc (`Fig. 6d`) | figure-read ≈1130 (최고) → ≈790 · 본문 **72 %** | figure-read ≈1220 → ≈1050 · 본문 **90 %** (초록 '90.2 %') | DOL/DME+LiNO₃ ≈1300 → ≈600 (110 cyc 에서 끝) | 기준 사이클 미기재 |
| 0.5/0.2 C · 200 cyc (`Fig. 6e`) | 처음 35 cyc 는 0.1/0.1 C (≈1200–1250) → 0.5 C 로 바꾸자 ≈1100 → ≈330 (70 cyc) | figure-read 첫 ≈1040 → 3 cyc ≈950 → 50 cyc ≈970 → 200 cyc ≈910 · 본문 **95 %** | — | 95 % 는 ≈50 cyc 기준이면 맞고 첫 사이클 기준이면 ≈88 % (우리 산수) |
| 2/0.5 C · 300 cyc (`Fig. 6f`) | — | figure-read 첫 ≈1200 → ≈15 cyc **≈810** → 300 cyc ≈780 | — | 본문 "very stable" — 첫 사이클 기준 ≈65 % · 온도 미기재 (기본 30 °C 로 읽힘) |
| 5/0.2 C · 100 cyc | — | `Fig. S20` (안 봄) | — | 본문 "steady" |
| 율 (30 °C · `Fig. 6a`) — 방전=충전 율 | — | 0.1 C figure-read ≈1070 (하한 ≈1.2 V) · 1 C ≈990 (≈0.95 V) · 4 C ≈1000 (≈0.7 V) · 8 C ≈840 (≈0.5 V) · **10 C 583 (≈0.5 V)** | — | ⚠ 괄호 = 그 곡선이 끝난 전압 (figure-read) · 10 C 충전은 ≈3.0 V 평탄 → ≈4.0 V 까지 |
| 율 (55 °C · `Fig. 6b`) — 충전 0.5 C 고정 | — | 0.2 C ≈1250 · 1 C ≈1140 · 4 C ≈1020 · 8 C ≈840 · **12 C 692 · 16 C 494** (모두 1.0 V 까지 · figure-read 는 12·16 C 외) | — | 16 C 방전 곡선은 ≈2.0 V 에서 시작해 평탄 없이 1.0 V 로 내려간다 |
| 율 (55 °C · `Fig. S19` · 방전=충전 율) | **2.5 C 210** (본문 · 하한 1.0 V) · 2 C figure-read ≈720 | 10 C figure-read ≈870 (**≈0.2 V 까지**) · 8 C ≈1000 (≈0.3 V) | DOL/DME+LiNO₃ 10 C figure-read ≈290 (**1.5 V 까지**) · 0.1 C ≈1250 (1.7 V) / LHCE 2 C ≈220 (≈1.4 V) | `Fig. S19c–f` · 20 mM BDTS 10 C ≈170 (≈0.2 V) · 100 mM 10 C ≈170 (0.5 V) |
| 문헌 대비 (`Fig. 6c` · `Table S2`) | — | 10 C 583 (30 °C) · 16 C 494 (55 °C) | 문헌 QSSSR 셀 "> 2.5 C 에서 100–300 mAh g⁻¹" | ⚠ 문헌 셀의 하한 전압 · 온도 · E/S 를 표에 적지 않았다 (`Table S2` 숫자 열은 글자층에서 빠져 우리는 못 옮겼다) |
| 희박 · 용량 고정 (55 °C · Extended Data Fig. 1a) | — | 2.0 mg cm⁻² · E/S 5.0 · 0.3/0.2 C · **800 mAh g⁻¹ 고정** · 210 cyc | — | CE figure-read ≈100 % · 고정 없이 (1.9–3 V · 0.2/0.1 C) 는 `Fig. S22` (안 봄) |
| (b) | — | 3.0 mg cm⁻² · E/S 5.0 · 0.3/0.1 C · 800 고정 · 100 cyc | — | — |
| (c) | — | 5.1 mg cm⁻² · E/S 4.0 · 0.1/0.1 C · **3.75 mAh cm⁻² 고정** (figure-read ≈3.74 · 본문 "3.7") · 50 cyc | — | 우리 산수: 3.75 / 5.1 = **≈735 mAh g⁻¹** |
| 파우치 (40 °C · Extended Data Fig. 1d · `Table S3` · `Table S4`) | figure-read ≈2300 → 10 cyc ≈760 mAh | **2.4 Ah · 331 Wh kg⁻¹** (포장 포함) · 423 Wh kg⁻¹ (포장 · 탭 제외) · figure-read 1 cyc ≈2350 → 24 cyc ≈1630 mAh (≈69 %) · CE ≈93–97 % | — | 4 mg cm⁻² (한 면) · E/S **3 µL mg⁻¹** · N/P 1.87 · S 분율 63.8 % · 양극 68 × 96 mm × 4 장 (양면) · Li 71 × 99 mm × 5 장 · 분리막 16 µm · Al 13 µm |
| 파우치 검산 (**우리 산수**) | — | S 질량 ≈2.09 g (8 면 × 65.28 cm² × 4 mg) · 이용률 ≈1149 mAh g⁻¹ · 함의 평균 전압 331 × 15.57 g / 2.4 Ah ≈ **2.15 V** · 포장 제외 331 × 15.57 / 12.21 ≈ 422 Wh kg⁻¹ ✓ (본문 423) · 전해액 3 µL mg⁻¹ × 2089 mg ≈ 6.27 mL ↔ 6.00 g (밀도 ≈0.96 g mL⁻¹ 이면 맞다) · S 분율 0.85 × 0.75 = 63.75 % ✓ | — | `Table S4`: 전극 + 분리막 6.21 g · 전해액 6.00 g · 포장 + 탭 3.36 g · 합 15.57 g |

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 전해질
- CPME · DOL · DME · THF (J&K) 4 Å 분자체 **7 일 이상** 건조 · LiTFSI (TCI) 130 °C 진공 72 h · LiNO₃ (Innochem) · **BDTS (Aladdin)** · 수분 (Karl Fischer) 미기재.
- `LiTFSI–CPME` = 1 mol L⁻¹ LiTFSI in CPME · `BDTS–LiTFSI–CPME` = 여기에 50 mmol L⁻¹ BDTS · DOL/DME = 1 M LiTFSI + 2 wt% LiNO₃ (1:1 v/v) · MTHF · THF 계 HLCE = 정해진 몰비 + 톨루엔 또는 하이드로플루오로에테르 희석.
- BDTS 정체 (**우리 식별 · 논문에 없는 이름**): bis(dimethylthiocarbamyl) sulfide = 테트라메틸티우람 모노설파이드 (C₆H₁₂N₂S₃ · ≈208 g mol⁻¹). 50 mM ≈ 10.4 g L⁻¹ → 전해액 밀도 ≈1.1 g mL⁻¹ 이면 ≈0.9 wt% (논문 `Table S5` 의 "0.9 wt%" 와 맞는다).
- **BDTSRed 용액** (UV–vis 용): 1 M LiTFSI 를 지지염으로 BDTS 용액을 LSV 0.05 mV s⁻¹ 로 전기환원 (활성화 사이클과 같은 절차) · 그 뒤 S₈ · Li₂S₆ · Li₂S 를 정해진 몰비로 넣고 24 h 저은 상등액.

### 4b. 전극 · 시약
- **S/탄소 복합체**: S + Ketjen black (XFNANO · 또는 정렬 CNT · 활성탄 — `Fig. S24`) 155 °C 12 h 용융 확산 · 70 wt% S → 복합체 : Super P : PVDF (Arkema) = 8:1:1 · 탄소 코팅 Al · 60 °C 12 h. 면적 부하는 그림마다 (기본은 미기재 · 희박 시험 2.0–5.1 mg cm⁻²).
- **Li₂S₆ 고체**: "lithium borohydride 와 S₈ 를 **8:3 몰비**" 로 반응 → 2 h 교반 → 60 °C 진공 12 h. 우리 산수: Li : S₈ = 8 : 3 → Li₈S₂₄ = 4 Li₂S₆ 로 화학량이 맞는다 (S 원자 기준으로 읽으면 Li₂S₅.₃ 이 되므로 'S₈ 분자' 기준 읽기가 맞다).
- **파우치 양극**: S/그래핀 (75 wt% S · 그래핀은 ref 56 절차) 85 + CNT 4 + Super P 6 + LA133 5 wt% (수계 · –CN 기 접착) · Al 박 · 양면 4 mg cm⁻² (한 면).

### 4c. 전기화학
- **코인**: CR2032 · Celgard 2500 · Li · E/S **10 µL mg⁻¹** · **30 °C** (달리 적지 않으면) · Neware CT-4008T-5V10mA-164. **방전 · 충전 차단 전압은 Methods 에 없다** — 그림마다 다르다 (§10-①).
- **GITT**: 0.05 C 펄스 20 min + 휴지 2 h.
- **Li\|Li · Li\|Cu**: 0.5 mA cm⁻² · 2 mAh cm⁻² · Li\|Cu 상한 1 V · 전해액 60 µL.
- **EIS**: Gamry Interface 1000 · Li\|Li 1 Hz–500 kHz · 10 mV / Li–S 10 mHz–100 kHz · 5 mV. Li–S 등가회로 R1–(R2‖CPE1)–(R3‖CPE2)–W_s (`Fig. S14b`).
- **LSV/Tafel**: S₈ 전극 · Li 상대 전극 · 0.1 mV s⁻¹ · 전극 면적 · 평형 전위 (과전압 원점) 미기재.
- **'착물화 반응 속도'**: 1 mL 50 mM BDTSRed + 10.3 mg Li₂S₆ · 30 °C 자석 교반 · 끝점 = 용액이 '완전히 맑아질 때' (육안).

### 4d. 분석
- **Raman** DXRxi · 532 nm. **⁷Li NMR** 400 MHz (AV III HD 400) · 3 mm 관 · 외부 기준 0.1 M LiCl/D₂O (5 mm 동축관). **UV–vis** Cary (Agilent). **점도** Anton Paar SVM 3001 (밀도) · MCR102e 레오미터 (점도). **XPS** ESCALAB 250Xi. **SEM** Hitachi SU-8200.
- **operando XRD**: Rigaku SmartLab 9 kW · Cu Kα · 20–60° · 0.01° 간격 · 2.5° min⁻¹ · Be 창 자작 셀 · 자립 양극 (S/KB : Super P : PTFE = 8:1:1 · **2–2.5 mg cm⁻²**) · **0.03 C** · 한 사이클 ≈150 패턴 · Li₂S 결정자 크기 = (111) 봉우리 (Scherrer 로 보임 · 식 · 기기 퍼짐 보정 미기재). `Fig. 5c` 정규화: 방전 시작 S₈ · 방전 끝 Li₂S 를 각 100 % (적분 반사 · 적분법 미기재).
- **operando XANES**: S K-edge · BSRF 4B7A · 형광. 선형결합맞춤 없음 (봉우리 위치 정성 판독).

### 4e. 계산 (전부) ★

| 계산 | 적힌 것 | 안 적힌 것 |
|---|---|---|
| **AIMD** (`Fig. 2c–g` · `Fig. S1d` · `Fig. S2` · `Fig. S5b,c` · 영상 1 · 2) | PAW · PBE · DFT-D3 · ENCUT **400 eV** · **Γ 점만** · 4 계 (1 M CPME 9:1 · 2 M 9:2 · 3 M 9:3 · 1 M DME 9:1 몰비 · 374/406/438/320 원자 · 16 / 16.5 / 17 / 15 Å 입방 · "실험 밀도로") · **303 K** · NVT · Nosé–Hoover · **평형 10 ps** · 1 fs · 1 M CPME 는 시작 구조 3 가지 (고체 LiTFSI 꼴 / 4 배위 — **400 K** / Li–TFSI 분리) | **코드 이름** (PAW 라 VASP 로 보인다 · 미기재) · D3 감쇠형 · **생산 구간 길이** ("after equilibrium" 만) · RDF/CN 평균 구간 · 배위 판정 절단 반경 (그림 점선 ≈2.9 Å (CPME) ↔ ≈3.3 Å (DME) — 계마다 다르다) · 시드 · 3 M 상자 길이 (Methods 오기) · (THF)₃–LiTFSI AIMD (`Fig. S5b,c`) 의 조건 전부 · 400 K 런의 생산 온도 |
| **고전 MD** (`Fig. S4`) | LAMMPS · Nosé–Hoover 100 fs · Anderson 기압계 1000 fs · PPPM · 힘장 = LigParGen (OPLS-AA · 1.14*CM1A-LBCC 전하) + 문헌 (Canongia Lopes–Pádua TFSI⁻ · Kamphaus–Balbuena) · LB 혼합 · NPT 1 ns (1 bar) → NVT **303 K 5 ns** · 1 fs · 1000 스텝마다 저장 · 0.25/1/2/3 M (3500/3740/4060/4380 원자) · DME 1 M (3200) · 매개변수 전부 `Table S6`–`S9` | 전하 크기 조정 (scaled charge) 여부 — OPLS 정전하로 보인다 · 배위 분율은 "몇 프레임을 무작위로 뽑아" 셈 (프레임 수 미기재) · 절단 반경 |
| **연속 용매화 에너지** (`Fig. S3`) | Quantum ESPRESSO 7.2 + **Environ 3.1** · SCCS · NCPP **SG15** · ecutwfc **60 Ry** (본문 '780 eV' = 57 Ry 가 아니라 60 Ry ≈ 816 eV — 괄호 환산도 어긋난다) · ε = 4.76 (CPME) · ΔG_sol = G_el − G₀ (용매 속 − 진공 총에너지) | 상자 크기 · 진공 · 범함수 (PBE 로 보임 · 미기재) · 클러스터 기하 (AIMD 스냅숏? 최적화?) · 비정전 항 (공동 · 분산) 매개변수 · 전하 상태 (클러스터 Li–TFSI–nCPME 는 중성) |
| **클러스터 DFT** (`Fig. 4c,d` · `Fig. S10` · `Fig. S11`) | B3LYP · **6-31+G(d,p)** · IEFPCM · D3(BJ) · 기하 최적화 · 시작 구조 "AIMD 에서" · E_b = E_total − E_BDTSRed − E_Li₂Sₓ · LUMO 그림 · Mulliken 전하 | 코드 (Gaussian 으로 보임 · 미기재) · IEFPCM 용매 (CPME? ε?) · BSSE · 진동 (ΔG) · 배좌 탐색 · **BDTSRed 의 전하 상태** (그림은 Li 가 붙은 중성 꼴 + "ionized state" 둘 다 언급 · `Fig. S10`) · 라디칼 계산의 스핀 · "AIMD 에서 시작" — AIMD 상자엔 BDTS 가 없다 |

> 원자 수 단서 (우리 산수): 1 M AIMD 상자에 Li⁺ 가 **2 개**다. `Fig. 2e` 의 "55.2 % / 43.6 %" 는 Li⁺ 두 개의 시간 평균이다. 고전 MD 상자 (Li⁺ 20 개 · 5 ns) 는 표본이 10 배 · 시간이 수백 배 많다.

### 4f. 파우치
- 양극 4 장 (양면 · 68 × 96 mm) · Li 5 장 (125 µm · 71 × 99 mm) · PE 분리막 16 µm · Al 13 µm · 알루미늄 적층 파우치 · E/S 3 µL mg⁻¹ · N/P ≈1.87 (Li 3860 · S 1672 mAh g⁻¹ 가정) · **40 °C**.
- 비에너지 W_G = Q × U / M (Q 셀 용량 · U 평균 전압 · M 셀 무게).
- N/P 검산 (**우리 산수** · Li 밀도 0.534 g cm⁻³): Li 125 µm ≈25.8 mAh cm⁻² · 양극 한 면 6.69 mAh cm⁻² → 안쪽 Li 한 장이 양극 두 면을 맡는다고 세면 ≈1.93 · 전체 Li / 전체 S 로 세면 ≈2.6. 1.87 은 앞쪽 셈법에 가깝다 (`shen2026` 과 같은 셈 · 같은 셀 설계).

---

## 5. 결과 — 절별 상세 (그림 실독 포함 · 모든 수치)

### 5.1 기본 WSE 의 용매화 — 분광 (`Fig. 2a,b`, `Fig. S1`)
- **Raman** (`Fig. 2a` 실독): S–N–S 띠 중심 DME figure-read ≈741 · CPME ≈747 · 고체 LiTFSI ≈747 cm⁻¹ — CPME 의 TFSI⁻ 가 고체염처럼 Li⁺ 에 강하게 배위.
- **맞춤** (`Fig. S1a,b` · SI 본문): CPME = 단자리 CIP 31.6 % + 두자리 CIP 68.4 % ("거의 100 % CIP") · DME = SSIP 50.0 % + 단자리 41.0 % + 두자리 9.0 %. 본문은 이를 "exclusive formation of CIP" vs "SSIP ~50 % · CIP ~50 %" 로 요약. 맞춤 조건 (선 모양 · 폭 고정) 미기재. `Fig. S1c` 는 MP 의 LiTFSI 결정 구조로 고체염 배위를 보인다.
- **⁷Li NMR** (`Fig. 2b` 실독): CPME figure-read ≈ −0.79 ppm (FWHM 2.156 Hz) · DME ≈ −1.16 ppm (FWHM 1.206 Hz). 저자 해석: 더 양의 이동 = 전자 차폐 감소 · 넓은 FWHM = Li 핵 주변 전자 밀도 비대칭↑ → TFSI⁻ 지배.
- **Li₂S₆ 용해도** ≈8 mM[S] (CPME) vs > 6 M (DME · 인용) — "세 자릿수 낮다". 측정은 "포화될 때까지 넣기" 로만 적혀 있다 (적정 · UV–vis 정량 없음).

### 5.2 AIMD — 3 배위 Li⁺ (`Fig. 2c–g`, `Fig. S2`, 영상 1 · 2)
- **결과** (`Fig. 2c,d` 실독): CPME 1 M — Li–O 첫 봉우리 figure-read ≈2.0 Å · 절단 점선 ≈2.9 Å · CN O(CPME) 1.98 + O(TFSI) 1.45 = **3.43**. DME 1 M — 절단 점선 ≈3.3 Å · O(DME) 3.00 + O(TFSI) 1.62 = **4.62**. Li–O(TFSI) g(r) 의 ≈4.2 Å 둘째 봉우리 = 같은 TFSI 의 다른 O.
- **배위 분포** (`Fig. 2e` 실독): CPME 2/3/4 배위 1.2 / **55.2** / 43.6 % · DME 4/5/6 배위 41.2 / **58.0** / 0.8 %. 대표 착물 (`Fig. 2f`): Li–TFSI–CPME (3 배위 · 두자리 CIP) · Li–TFSI–2CPME (3 배위 · 단자리 CIP) · Li–TFSI–2CPME (4 배위 · 두자리 CIP). DME (`Fig. 2g` · `Fig. S1d`): Li–3DME (4 · SSIP) · Li–TFSI–2DME (4 · 단자리) · Li–TFSI–3DME (5 · 단자리 / 4 · 단자리 / 5 · 두자리).
- **저자 주장**: "3 배위 Li⁺ 는 비수계 전해질에서 드물다" (실록산계 ref 33 · 370 K 카보네이트 ref 34 외) → CPME 의 약용매화 + 사이클로펜틸 입체 장애 때문.
- **농도 의존** (`Fig. S2b,c,f`): 2 M — 4 배위 54.0 % · 5 배위 5.0 % · CN 3.63 / 3 M — 4 배위 47.0 % · 5 배위 14.6 % · CN 3.76. 농도가 오르면 TFSI⁻ 참여가 늘어 CN 이 오른다.
- **시작 구조 시험** (`Fig. S2d,e` 실독 · 저자 동기: 시작 구조 의존을 지적한 *J. Phys. Chem. B* 2017 · 2018): (d) 4 배위 시작 · **400 K** ("완전한 평형을 위해") → 3/4 배위 53.8 / 46.2 % · CN 3.46. (e) Li 와 TFSI 를 떼어 놓고 시작 → 0.3 / 55.3 / 44.4 % · CN 3.44. 저자: "세 런 모두 비슷하다" → 3 배위 공존 확정.
  ⚠ **우리 실독**: 총 CN 은 같지만 **종별 분배가 다르다** — (a) CPME ≈2.0 / TFSI ≈1.4 · (d) CPME ≈1.4 / TFSI ≈2.0 · (e) CPME ≈1.9 / TFSI ≈1.4 (figure-read · 절단 ≈2.9 Å). 이 논문의 논지 (TFSI⁻ 지배 → CIP → 약용매화) 에 필요한 것은 **종별** 분배인데, 그게 시작 구조에 따라 움직인다. (e) 에서 Li–O(TFSI) 누적 CN 이 5.5–7.5 Å 에서 정확히 4 로 평평한 것은 상자 안 TFSI⁻ 가 2 개 뿐이라 생기는 모양이다.
- **관측창 (우리 규율 · `D-2026-10-05-md-observation-window`)**: Ea₁ = kT·ln(ν₀·t·n) · ν₀ 10¹³ s⁻¹ **가정** · T 303 K (kT 0.0261 eV) · t = 10 ps (논문에 적힌 유일한 길이 · 생산 구간 미기재) · n = 2 (Li⁺ 두 개) → **기대 사건 1 ≈ 0.14 eV (검출 63 %) · 95 % 검출 ≈ 0.11 eV**. 리간드 교환 (CPME ↔ TFSI⁻ 자리 바꿈) 장벽이 이보다 크면 한 런 안에서 거의 안 일어난다 — 시작 구조마다 종별 분배가 달라진 (d)/(a) 관측과 맞는 그림이다.
- **고전 MD 대조** (`Fig. S4` · SI 본문 · 안 봄): CPME 0.25/1/2/3 M CN 4.00/4.07/4.24/4.27 · 3/4/5 배위 1 M 7.5/81.0/11.5 % · DME 5.65. 추세 (농도↑ → TFSI 참여↑ · CPME < DME) 는 AIMD 와 같지만 **절대 CN 이 0.6–1.0 높다**. 저자 처리 (`Supplementary Note 1`): 문헌 6 건 (G3 · DOL/DME · DME/BTFE · G2 · LiFSI-DME-BTFE) 에서도 고전 MD CN 이 AIMD 보다 높고, *J. Chem. Phys.* 161, 054504 (2024) 가 글라임에서 고전 MD 과대평가를 직접 보였다 → "AIMD 가 더 정확" 으로 결론. 그리고 "CPME 검토는 이 논문의 큰 목표에 영향이 없다" 고 덧붙인다 (심사 대응 흔적으로 읽힌다).
  우리 판정: 고전 MD 과대평가 가설은 성립할 수 있지만, 이 논문 안에서는 **AIMD 쪽 통계 (Li⁺ 2 개 · 생산 길이 미기재 · 시작 구조 의존)** 가 같은 크기의 대안 설명이다 — 둘을 가를 시험 (예: AIMD 상자 2 배 · 시드 셋 · 고전 MD 전하 0.8 배 조정) 이 없다.

### 5.3 연속 용매화 '열역학 검증' (`Fig. S3` 실독)
- 3 배위 = Li–TFSI–CPME (CPME 1) · 4 배위 = Li–TFSI–2CPME (CPME 2) 클러스터 (`Fig. S3a,b` 그림).
- ΔG_sol (QE-Environ SCCS · ε 4.76): 4 배위 −0.0453 Ry (−28.4814 kcal/mol) · 3 배위 −0.0188 Ry (−11.8546 kcal/mol) → "둘 다 음수이니 CPME 속에 열역학적으로 존재할 수 있다".
- 저자 스스로 SI 에 "ΔG_sol 의 절대값은 서로 다른 구조 비교에 못 쓴다" 고 적었다.
- ⚠ 우리 판정 (§10-⑤ · ⑥): 극성 클러스터를 ε > 1 연속체에 넣으면 ΔG_sol 은 거의 언제나 음수다 — 이 부호는 '3 배위가 존재한다' 와 무관하다. 물어야 할 것은 Li–TFSI–CPME + CPME(용액) → Li–TFSI–2CPME 의 반응 자유에너지 (같은 연속체 안) 다. 그리고 −0.0453 Ry 는 −14.2 kcal/mol (1 Ry = 313.75 kcal/mol) 이지 −28.5 가 아니다 — 적힌 kcal 값은 Hartree 환산 (0.0453 Ha × 627.5) 과 일치한다.

### 5.4 저밀도 · 저점도와 Li 금속 (`Fig. 3c–e`, `Fig. S5`, `Fig. S6`)
- **점도** 1.24 mPa s (`Fig. S5a` · 안 봄) — DOL/DME+LiNO₃ 와 비슷 · 농후 THF 계 · 희석 LHCE 보다 훨씬 낮다. `Fig. S5b,c` (AIMD (THF)₃–LiTFSI): SSIP Li⁺–4THF · 두자리 CIP Li⁺–2THF–TFSI · 응집체 2Li⁺–4THF–2TFSI → "CPME 의 Li–2CPME–LiTFSI 착물이 더 작아 수송에 유리".
- **SEM** (`Fig. 3c,d` 실독): CPME = 크게 융합된 섬 · 치밀 / DME = 느슨한 입자. 0.5 mA cm⁻² · 2 mAh cm⁻².
- **Li\|Cu** (`Fig. S6a–c`): 평균 CE ≈98.4 % (CPME) · 66.3 % (그림) / 66.7 % (본문) (DME).
- **Li\|Li** (`Fig. 3e` 실독): CPME 600 h 단락 없음 · 과전압 figure-read ≈0.08 → ≈0.15 V 로 늘어 가는 '부드러운' 곡선 (삽입 554–558 h ≈ ±0.15 V) / DME figure-read ≈ ±0.02–0.03 V → ≈300 h 이후 진폭 출렁 (±0.07 V · 삽입 540–546 h ±0.08 V). **두 패널 y 축 범위가 다르다** (CPME ±0.4 · DME −0.1–0.2).
- **XPS** (`Fig. S6d–k` · 안 봄): CPME SEI 에 F · S · N 이 많다 · LiF · Li₂SₓO_y · Li–N → 무기 풍부 SEI (TFSI⁻ 우선 분해).
- **EIS 70 일** (`Fig. S6l` · 안 봄): R2 증가 CPME +6.7 % · DME +104 % — 단, CPME 쪽 R2 절대값이 더 크다 (SI 본문).

### 5.5 상 매개자 BDTS — 산화환원 · 착물 (`Fig. 4a–d`, `Fig. S7`–`S11`)
- **BDTS 자체가 산화환원 활성** (`Fig. 4a` 실독 · `Fig. S7`): BDTS 단독 (50 mM · 탄소종이) — 첫 방전에 ≈1.5–1.6 V 긴 평탄 = '활성화' (CV 1.439 V) · 그 뒤 두 단 환원 (CV 2.416 · 2.196 V) · 산화 2.659 V (`Fig. S7c` 인쇄). S₈ 는 환원 2.132 · 1.820 V · 산화 2.494 V (`Fig. S7d`). → **방전 때 BDTS 가 S₈ 보다 먼저 환원, 충전 때 Li₂S/LiPS 보다 나중에 산화** = 닫힌 순환의 근거 (`Fig. 4a` 에서 BDTS 방전 곡선 (2 번째) 이 S₈ 곡선보다 위 · 충전 곡선이 S₈ 위).
- **BDTS 단독 율 · 사이클** (`Fig. S8` · 안 봄): 0.1–4 C · 1 C 장기 · 1.0 mg cm⁻² — "초고율 · 빠른 산화환원".
- **용해 착물** (`Fig. 4b` · `Fig. S9` 실독): 50 mM BDTSRed 가 고체 Li₂S₆ 를 녹인다 · 최대 BDTSRed : Li₂S₆ = **1:3** (`Fig. S9b` 사진 — 1:1 · 1:2 · 1:3 · 1:4 병 모두 바닥에 흰 교반자 · 1:4 는 탁하다는 판단이 사진에서 뚜렷하지는 않다) → Li₂S₆ ≈150 mM. UV–vis (5 mM 로 희석): S₆²⁻ ≈350–360 · S₄²⁻ ≈435 · S₈²⁻ ≈550 · S₈ ≈293 nm · 1:3 에서 S₃•⁻ ≈620 nm 넓은 흡수 · 24 h 뒤 빨갛게 변하며 S₈²⁻ 증가 (`Fig. S9d`) — 불균화 2S₆²⁻ ⇌ S₈²⁻ + S₄²⁻ · 4S₆²⁻ ⇌ S₈ + 4S₄²⁻ · S₆²⁻ ⇌ 2S₃•⁻.
  ⚠ 우리 실독: `Fig. S9a` 의 BDTS 와 BDTSRed 스펙트럼이 **거의 같다** (≈246 · ≈338 · ≈405 nm · 세기만 조금 다름 — SI 본문도 "nearly the same" 인정). C–S 결합이 끊어진 디티오카르바메이트라면 기대되는 흡수 변화가 안 보인다 — '환원체' 의 정체를 분광으로 확인하지 못했다. 또 BDTSRed 띠 (≈250 · ≈340 · ≈405 nm) 가 S₈ · S₆²⁻ · S₄²⁻ 띠와 겹치고 흡광도가 > 2 라 배정이 흔들린다.
- **S₈ · Li₂S 와는 안 붙는다** (`Fig. S9e,f` 실독): 상등액에 새 띠가 없다 → "착물이 Li₂S · S₈ 가 되면 풀린다". ⚠ `Fig. S9e` 의 BDTSRed + S₈ 스펙트럼은 ≈405 nm 어깨와 ≈245 nm 가 BDTSRed 단독보다 **커졌다** — '변화 없음' 이라기엔 차이가 있다.
- **환원 기전 (DFT)** (`Fig. 4c` · `Fig. S10` · `Fig. S11`): BDTS 의 LUMO 가 C–S 결합을 따라 있다 → 환원 시 C–S 절단 → 라디칼 I (Me₂N–C(S)–S•) · 라디칼 II (Me₂N–C•=S) → 각각 전자 1 · Li⁺ 1 을 받아 BDTSRed I (디티오카르바메이트) · BDTSRed II. Mulliken: 라디칼 I 의 두 S (S10 · S12) 가 거의 같은 음전하 → 금속 킬레이트 가능 · 라디칼 II 는 S9 · C8 이 음전하. 공명형 (디티오카르바메이트 ↔ 티오우레이드) 으로 N 은 전자 부족 · S 는 전자 풍부 (`Fig. S11a`).
- **결합에너지** (`Fig. 4d` 실독): BDTSRed I–Li₂S₆ figure-read ≈ −1.9 (I) · ≈ −2.1 eV (I′) · BDTSRed II–Li₂S₆ ≈ −1.7 (II) · ≈ −2.45 eV (II′). 그림의 BDTSRed I · II 는 **Li 가 붙은** 분자로 그려져 있고 (Li–S₂CNMe₂ · Li–C(S)NMe₂), 착물에서는 BDTSRed 의 S 가 Li₂S₆ 의 Li 에 · Li₂S₆ 의 S 가 BDTSRed 의 Li 에 붙는다 ("반대 방향 착물도 있다" — 본문).
- **우리 규율 (`D-2026-10-05-adsorption-site-coordination`) 적용**: ≈2 eV 는 화학결합 규모다. 결합 상대가 **기상 (연속 용매) 고립 Li₂S₆ 클러스터** 라 Li 가 저배위다 — 이 값은 '저배위 Li₂S₆ 의 결합 포화 에너지' 로만 읽힌다. 논문이 말하는 '**고체** 준고체 Li₂Sₓ 의 **표면**' 착물화를 모형화한 것이 아니다. 그리고 경쟁 상대 (CPME · TFSI⁻ 가 같은 Li₂S₆ 에 붙는 에너지) 를 같은 수준으로 안 냈다 — 왜 BDTSRed 가 이기는지는 계산으로 보이지 않았다.

### 5.6 동역학 증거 (`Fig. 4e`, `Fig. S12`–`S15`)
- **GITT** (`Fig. S12a` 실독): BDTS 셀도 2.2 V 준이중 평탄 · ≈400 mAh g⁻¹ 에 전압 골 (닫힌 회로 figure-read ≈1.92 V) · 충전 과충전 없음 → "전체로는 여전히 QSSSR".
- **용해 분율 추정**: Li₂S₆ 150 mM 을 E/S 5 µL mg⁻¹ 로 가정하면 셀 전체 S 의 **≈15 wt%** 가 녹는다 (본문 · SI). 우리 검산: 150 mM × 6 = 0.9 M[S] × 5 µL = 4.5 µmol S = 0.144 mg per mg S ✓ (14.4 %). ⚠ 실제 코인셀 기본 E/S 는 **10 µL mg⁻¹** (Methods) → 같은 셈으로 **≈29 %**.
- **S₈ 셀의 1 · 2 번째 사이클** (`Fig. S12b` 실독): 2 번째 사이클 시작에 ≈2.45–2.5 V 짧은 평탄 (BDTS 환원 · figure-read ≈50–60 mAh g⁻¹(S)) · 충전 끝 ≈2.4–2.6 V 기울기 (BDTSRed 산화). 1 번째 사이클 곡선 (검정) 에는 시작 평탄이 거의 없다.
  BDTS 용량 몫 (**우리 산수**): 50 mM × 10 µL mg⁻¹ = 0.5 µmol BDTS per mg S · 분자당 2 e⁻ (라디칼 둘 × 1 e⁻) 이면 ≈27 mAh g⁻¹(S). 그림의 ≈50–60 은 그 두 배쯤 — 전자 수 · 실제 E/S 가 다르거나 BDTS 외 기여가 섞였다. 어느 쪽이든 **고율에서 용량의 수 % 이상이 S 가 아닌 BDTS 몫**일 수 있다 (10 C 583 mAh g⁻¹ 의 ≈5–10 %).
- **Tafel** (`Fig. S13` 실독): S₈ LSV (0.1 mV s⁻¹) — BDTS 셀 전류가 2.16–2.28 V 에서 더 크다 (2.16 V 에서 figure-read ≈ −0.31 vs ≈ −0.13 mA). Tafel 맞춤은 과전압 **0.080–0.090 V** (10 mV) 에서 기울기 figure-read ≈125 (CPME) · ≈110 mV dec⁻¹ (BDTS). 우리 검산: log j₀ = log j(0.080) − 0.080/b → CPME −1.02 − 0.64 = −1.66 (j₀ ≈0.022) ✓ · BDTS −0.63 − 0.72 = −1.35 (≈0.045) ✓ — 숫자는 맞다.
  ⚠ 그러나 (i) 10 mV 창에서 낸 기울기로 80 mV 를 외삽했고, (ii) 과전압 원점 (2.28 V?) 이 정의되지 않았고, (iii) 그 전위 창 (2.16–2.28 V) 에 **BDTS 자신의 환원 봉우리 2.196 V** (`Fig. S7c`) 가 걸린다 — 셀을 먼저 활성화했는지 적혀 있지 않다. 늘어난 전류가 S₈ 환원인지 BDTS 환원인지 가를 수 없다.
- **'착물화 속도'** 1.38 × 10⁻⁵ mol L⁻¹ s⁻¹ (SI): 우리 산수 — 50 mM 을 다 녹이는 데 ≈3600 s (≈1 h). 2 C 방전 (≈30 min) · 10 C (≈6 min) 보다 **길다**. 고체 분말 10.3 mg 의 용해 (교반 · 물질전달) 를 육안 끝점으로 잰 값이라 '표면 착물화 속도' 를 잰 것도 아니다. 본문은 이를 "very fast" 라 적었다.
- **Li₂S 활성화** (`Fig. S14a` 실독): 미세 Li₂S 양극 (먼저 한 번 방전해 BDTS 를 BDTSRed 로) — 첫 충전 장벽 BDTS ≈3.23 V vs CPME ≈3.72 V. BDTS 셀은 장벽 앞에 ≈2.5 V 계단 (figure-read ≈40–50 mAh g⁻¹(Li₂S) — BDTSRed 산화) 이 먼저 지나간다. 저자: BDTSRed 가 산화 개시 때 생기는 미량 LiPS 를 녹여 장벽을 낮춘다.
- **EIS** (`Fig. S14b,c` 실독): 반 방전 셀 · R1 ≈28 Ω (둘 다) · R2 ≈130 → ≈53 Ω · R3 ≈172 → ≈151 Ω (figure-read). Nyquist 는 한 셀 것만 그려져 있다 (어느 전해질인지 표시 없음).
- **LiI (고전적 RM) 대조** (`Fig. S15` · 안 봄 · 55 °C): 20 · 50 mM LiI 는 BDTS 없는 셀보다 조금 낫고 BDTS 보다 못하다 → "상 매개가 RM 보다 효과적".
- **다른 SSE 에도** (`Fig. S16` · 안 봄): (THF)₂–LiTFSI + 50 vol% HFE · (DOL-DME)₂–LiTFSI + 40 vol% 톨루엔에 50 mM BDTS → 사이클 개선 ("보편적 · 정도는 계마다").

### 5.7 황 종 동역학 — operando XRD · XANES (`Fig. 5`, `Fig. S17`, `Fig. S18`)
- **등고선** (`Fig. 5a,b` 실독): 방전 ≈15 h · 충전 ≈21 h. 방전 초 α-S₈ (≈21.8 · ≈23.0 · ≈26.6°) 가 ≈4 h 안에 사라지고 Li₂S (≈26.9°) 넓은 띠가 뒤에 선다. 충전 ≈11–12 h 에 α-S₈ (23.0°) 가 다시 강하게 선다.
  ⚠ **캡션은 "LiTFSI–CPME 셀"** 인데 같은 논문은 LiTFSI–CPME 의 재충전 상을 **γ-S₈** 라 하고 (`Fig. 5d` · `Table S1`), 실제 LiTFSI–CPME 등고선 `Fig. S17a` (실독) 에는 충전 끝에 γ-S₈ (Δ ≈24.0 · ≈25.6 · ≈27.2 · ≈29.0°) 이 선다 (총 ≈40 h). `Fig. 5a,b` 의 α-S₈ 재생 · 짧은 시간 축은 BDTS 셀 쪽 서술과 맞는다 — **캡션의 전해질 이름이 틀렸을 가능성이 크다**.
- **정규화 세기** (`Fig. 5c` 실독): 표 §3c. 요지 — BDTS 셀은 S₈ 가 DME (캐솔라이트) 만큼 빨리 사라지고 (≈20 % DOD 에서 figure-read ≈85 % 소비), CPME 셀은 ≈25 % DOD 까지 S₈ 가 거의 그대로 있다가 갑자기 사라진다. 결정 Li₂S 는 DME ≈35 % → CPME ≈47 % → BDTS ≈51 % DOD 순으로 늦게 보인다. 충전 때 BDTS 셀은 S₈ 가 ≈58 % SOC 에 다시 보인다 (Li₂S 가 ≈30 % 남은 상태). 정규화가 각 상의 최대값 기준이라 **결정 Li₂S 의 절대량** 은 셀 사이에 비교되지 않는다.
- **Li₂S 결정자** (`Fig. S17d,e` 실독): (111) 봉우리 · DME ≈10.8 · CPME ≈13.3 · BDTS ≈11.8 nm (막대) · 점 다섯 = 같은 셀의 마지막 XRD 5 장 (표본 = 측정 반복이지 셀 반복이 아니다).
- **재충전 황** (`Fig. 5d` 실독): 처음 양극 α-S₈ ((222) ≈23.0° · (220) · (311)) / BDTS 셀 α-S₈ ((222) 가 강함) / CPME 셀 γ-S₈ ((022) ≈27.2° · (121)/(200) · (130) · (220)) / DME 셀 β-S₈ ((130)/(031) ≈25.8° · (−221) · (300) · (041)/(140) · (−411)). 저자: γ-S₈ 의 전기화학 생성은 드물다 (용액 · 용융물 또는 탄소 미세기공에서만 보고) · α-S₈ 생성은 표면 국소 용액에서 석출되는 다른 핵생성 에너지 지형 때문. `Table S1` 은 문헌 13 계의 재충전 상을 반응 기전 (캐솔라이트 · QSSSR) 별로 정리 — 캐솔라이트는 대개 β-S₈ · QSSSR 은 α-S₈ 이 많다.
- **SI `Fig. S17b,c`** (실독): 캡션은 "LiTFSI–CPME 의 방전 · 충전 폭포 그림" 인데 패널 안 라벨은 **"LiTFSI-DME"** 이고, 충전 끝에 Δ (γ-S₈) 가 선다 — γ-S₈ 는 CPME 쪽 서술이므로 패널 라벨이 틀린 것으로 보인다. SI 본문 "Li₂S 소비 속도는 두 전해질에서 비슷하다" 의 '두 전해질' 도 어느 둘인지 모호하다.
- **XANES** (`Fig. S18` · 안 봄 · SI 본문): BDTS 셀 (1 사이클 활성화 뒤) 방전 350 mAh g⁻¹ 에서 LiPS 전가장자리 ≈2470.7 eV · Li₂S ≈2476.2 eV → "QSSSR 에도 LiPS 가 생긴다 (S₈ ↔ Li₂S 직행이 아니다)". 충전 400 mAh g⁻¹ 스펙트럼도 있다.

### 5.8 셀 성능 (`Fig. 6`, Extended Data Fig. 1, `Fig. S19`–`S24`, `Table S2`–`S5`)
- **율 (30 °C · `Fig. 6a` 실독)**: 방전 = 충전 율 · 0.1 / 1 / 4 / 8 / 10 C. 각 곡선이 끝난 전압 (figure-read) 0.1 C ≈1.2 V · 1 C ≈0.95 · 4 C ≈0.7 · 8 C ≈0.5 · 10 C ≈0.5 V. 10 C 583 mAh g⁻¹ 은 **0.5 V 까지** 뺀 용량이다. 충전은 10 C 에서 ≈3.0 V 평탄 → ≈4.0 V 까지.
- **율 (55 °C · `Fig. 6b` 실독)**: 충전 0.5 C 고정 · 방전 0.2–16 C · 전부 **1.0 V 까지**. 16 C 494 · 12 C 692 (본문) · 8 C figure-read ≈840 · 0.2 C ≈1250. 고율 방전 곡선은 평탄이 없는 기울기다 (16 C ≈2.0 → 1.0 V).
- **`Fig. S19` (55 °C · 방전 = 충전 율 · 실독)**: BDTS 50 mM (f) — 10 C figure-read ≈870 mAh g⁻¹ 를 **≈0.2 V** 까지 · 충전은 ≈4.0 V 까지. BDTS 20 mM (a) — 6 C · 10 C 가 ≈0.6 · ≈0.2 V 까지 ≈170 · BDTS 100 mM (b) — 10 C ≈170 (0.5 V). BDTS 없음 (c) — 2.5 C 210 · 2 C ≈720 (**1.0 V 까지**). LHCE (d) — 2 C ≈220 (**≈1.4 V**). DOL/DME+LiNO₃ (e) — 10 C ≈290 · 8 C ≈480 (**1.5 V** · 저율 1.7 V) · 충전 중 출렁임 = "Li 덴드라이트".
  ⇒ 같은 그림 안에서 **비교 셀은 1.0–1.7 V · BDTS 셀은 0.2–0.5 V 까지** 방전했다. 우리 대충 판독: `Fig. S19f` 의 10 C 곡선은 ≈1.5 V 에서 시작하므로 DOL/DME 와 같은 1.5 V 하한이면 ≈0 mAh g⁻¹ 이다 (figure-read). 본문의 "BDTS 셀이 캐솔라이트보다도 율 성능이 낫다" 는 이 하한 차이를 빼면 성립하지 않는다 (§10-①).
- **농도 최적화** (`Fig. S19a,b` · SI 본문): 20 mM 은 4 C 까지 개선 · 50 mM 이 최적 · 100 mM 은 과용해로 활물질 손실 → 율 저하 (저자 해석).
- **문헌 비교** (`Fig. 6c` 실독 · `Table S2`): 이 연구 55 °C (빨간 실선 · 16 C 까지) · 30 °C (빨간 점선 · 10 C 까지) vs ref 55 · 66 · 61 · 24 · 11 (≤ 7 C). 문헌 셀의 하한 전압 · 온도는 표시 없음.
- **장기 사이클** (`Fig. 6d–f` 실독): §3d 표. `Fig. 6e` CPME 셀은 처음 35 cyc 를 0.1/0.1 C 로 돌린 뒤 0.5/0.2 C 로 바꿔 급락 (≈1100 → ≈330 · 70 cyc). `Fig. 6f` 2/0.5 C 는 첫 15 cyc 에 ≈1200 → ≈810 으로 ≈1/3 을 잃은 뒤 ≈780–900 사이를 오간다.
- **희박 · 고부하** (Extended Data Fig. 1a–c 실독 · 55 °C · **방전 용량 고정**): a 2.0 mg cm⁻² · E/S 5.0 · 0.3/0.2 C · 800 mAh g⁻¹ 210 cyc · b 3.0 mg cm⁻² · E/S 5.0 · 0.3/0.1 C · 800 · 100 cyc (CE ≈100 %, 88 cyc 근처 한 번 ≈95 %) · c 5.1 mg cm⁻² · E/S 4.0 · 0.1/0.1 C · ≈3.75 mAh cm⁻² · 50 cyc. 고정 없는 시험은 `Fig. S22` (1.9–3 V · E/S 5 · 0.2/0.1 C · 안 봄) · 전압 곡선 `Fig. S21` · `Fig. S23` (안 봄).
- **파우치** (Extended Data Fig. 1d 실독 · 40 °C): BDTS 첫 figure-read ≈2350 → 4 cyc ≈2150 → 7 cyc ≈1770 → 24 cyc ≈1630 mAh · CE figure-read ≈93–97 % (8 cyc 한 점 ≈105 %) / CPME ≈2300 → 10 cyc ≈760 mAh. 본문: "24 cyc steady" · "LiTFSI–CPME 파우치는 10 cyc 안에 망가진다". 사진 라벨 "Energy Density 331 Wh kg⁻¹ · Cell Capacity 2.4 Ah".
- **탄소 숙주** (`Fig. S24` · 안 봄 · SI 본문): KB (≈1400 m² g⁻¹ · 메조기공) > 정렬 CNT (≈180) > 활성탄 (≈3300 · 미세기공 > 95 %) — 미세기공은 BDTS · 전해액이 못 들어가 QSSSR 에 부적합.
- **가격** (`Table S5`): 1 M LiTFSI + 0.9 wt% BDTS in CPME 는 DOL/DME + 2 wt% LiNO₃ 보다 싸고 상용 카보네이트 전해액과 비슷 (단가 숫자는 글자층에서 빠짐).
- **향후** (`Supplementary Note 2`): 착물화/탈착물화 동역학 실측 · 촉매 숙주와의 결합 · 난연 전해질.

## 6. 메커니즘 · 논증 흐름 (`Fig. 1`, `Fig. 4f`) — 논증 사슬 판정

**저자 사슬**:
1. CPME 는 약용매화 (ε 4.76 · 한 자리 O · 사이클로펜틸 입체 장애) → 1 M 에서도 TFSI⁻ CIP 지배 · 3 배위 Li⁺ (Raman · NMR · AIMD) → LiPS 를 못 녹인다 (≈8 mM[S]) → 전체가 QSSSR (준이중 평탄 · 셔틀 없음).
2. 같은 용매화가 TFSI⁻ 우선 분해 → 무기 풍부 SEI → Li 금속 안정 (CE 98.4 % · 600 h).
3. 그러나 QSSSR 은 고체–고체 전하 이동이라 느리다.
4. BDTS 를 넣으면 첫 방전에서 C–S 절단 · 환원 → BDTSRed (디티오카르바메이트 · Li 와 킬레이트) (LUMO · Mulliken · 결합에너지 DFT).
5. BDTSRed 가 고체 Li₂Sₓ 표면의 Li⁺ 를 S 로 붙잡아 BDTSRed–Li₂Sₓ(sol) 을 만들고 (용해도 ≈150 mM · UV–vis), 표면 근처에서 빠른 용액상 반응이 돈다.
6. Li₂S · S₈ 와는 안 붙으므로 생성물이 되면 BDTSRed 가 풀려 다음 순환 (`Fig. 1c` 의 'Loop').
7. 증거: 교환 전류 2 배 · Li₂S 충전 장벽 ↓ · S₈ 소비 빨라짐 · 결정 Li₂S 늦게 · 더 작게 · 재충전 α-S₈ (다른 핵생성 경로) · 율 · 사이클 · 파우치.

**판정**:

| 고리 | 판정 | 이유 |
|---|---|---|
| 1 (약용매화 · QSSSR) | ✅ | 분광 · 용해도 · GITT 가 같은 방향. AIMD '3 배위' 는 부가 주장이고 통계가 약하다 (§5.2) — 결론 1 에 꼭 필요하지는 않다 |
| 2 (Li 금속) | ✅ (⚠ 과전압 증가) | CE · SEM · XPS 일치 · 단 Li\|Li 과전압이 시간에 따라 두 배로 는다 |
| 4 (BDTS → BDTSRed 정체) | ⚠ | LUMO 위치 → C–S 절단은 추론 · 환원 생성물을 NMR · MS · IR 로 확인하지 않았다 · UV–vis 는 BDTS 와 BDTSRed 가 거의 같다 |
| 5 (표면 국소 용액 반응) | 🔴 | **공간 국소성을 잰 측정이 없다.** 관측된 것은 '벌크 용해도 ≈8 → ≈900 mM[S] (≈110 배)' 와 'S₈ 소비가 캐솔라이트만큼 빠르다' 다. 같은 데이터가 **"BDTS 가 전해액을 중간 용해도 (≈0.9 M[S]) 의 미니 캐솔라이트로 바꿨다"** 는 단순한 대안과도 맞는다. 그 대안에서 '전체 QSSSR 유지' 의 근거는 GITT 모양뿐인데, E/S 10 µL mg⁻¹ 에서 S 의 ≈29 % (우리 산수) 가 녹을 수 있다 |
| 6 (닫힌 순환 · 탈착물화) | ⚠ | `Fig. S9e,f` 의 '상등액 변화 없음' 이 근거 · S₈ 혼합 스펙트럼은 실제로 조금 변했다 · 순환 횟수 (TON) 를 잰 것은 없다 |
| 상 매개 ≠ 산화환원 매개 | ⚠ | BDTS/BDTSRed 는 2.2–2.7 V 에서 산화환원한다. 충전 때 2.66 V 에서 생긴 BDTS (산화형) 가 Li₂S/LiPS 를 **화학적으로 산화**하는 고전 RM 경로가 열역학적으로 가능하다 (S 산화 2.49 V 보다 높다 · 우리 추론) · `Fig. S14a` 의 Li₂S 장벽 감소도 그 경로로 설명된다 · 배제 시험은 다른 분자 (LiI) 비교뿐 |
| 7 (성능) | ⚠ | 율 비교는 하한 전압 불일치 (§5.8) · 사이클 '유지율' 기준점 미기재 · 희박 시험은 용량 고정 + 55 °C (캡션에 밝힘) |

**한 문장**: Li 쪽과 '용해가 늘어 빨라졌다' 까지는 데이터가 받치고, '**표면에만**' 과 '**RM 이 아니다**' 는 이름이 데이터를 앞선다.

## 7. 우리 계산 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

> 이 논문은 황화물 SE 물성 (σ · Ea · ESW · 기계 · gap) 값을 하나도 안 낸다 — `comparison_vs_ours.md` 4 축 표에 행을 만들 대상이 아니다. 아래는 **방법 · 개념 · 보고 규약** 대조만이다. 우리 수치는 싣지 않는다 (위치만).

### 7a. 방법 대조 — 같은가 다른가

| 항목 | 이 논문 | 우리 | 같다/다르다 · 왜 |
|---|---|---|---|
| MD 힘 | AIMD PBE-D3 (Γ · 400 eV) · 고전 OPLS | UMA-s-1p1 (omat) MLIP-MD (`tools/modelc_v3/` · `tools/ionic/`) | 다르다 — 그들은 용매화 **구조 통계 (RDF · CN · 배위 분율)** 를 보고 우리는 **수송 (MSD → D · σ 상대비)** 을 본다 |
| 통계 단위 | Li⁺ **2 개** · 평형 10 ps · 생산 길이 미기재 · 시드 1 (시작 구조 3 가지는 1 M 만) | 결정계 558 원자 · 생산 200 ps · MSD 창 2–50 ps · 비율은 **멀티시드 판정만** (단일시드 1.33× 철회 선례) | 다르다 — 그들의 '3 배위 55 %' 는 우리 규율이면 **단일 시드 · 표본 2 의 값**이라 비율로도 인용 못 한다 |
| 방법 간 불일치 처리 | 고전 MD CN 이 AIMD 보다 0.6–1.0 높다 → 문헌 · 한 논문을 근거로 "고전 MD 가 과대평가" | (우리 규율) 판독 도구를 바꾸면 과거 마감부터 재현 · 대조 잡 | 다르다 — 우리 꼴이면 AIMD 상자 크기 · 시드 · 길이를 키워 AIMD 쪽 수렴을 먼저 보였을 것 |
| 연속 용매화 | QE 7.2 + Environ SCCS · SG15 · 60 Ry | QE 사용 (슬랩 · 벌크 DFT) · Environ 연속 용매화를 쓴 우리 기록은 이 digest 작성 중 확인하지 않았다 | — 그들의 쓰임 (ΔG_sol 부호로 존재 판정) 은 방법의 쓰임새가 아니다 (§5.3) |
| 분자 결합에너지 | B3LYP-D3(BJ)/6-31+G(d,p) · IEFPCM · BSSE · ΔG 없음 · 전하 상태 미선언 | ORCA r2SCAN-3c (SDCP 분자 계열 · desktop WSL) | 다르다 · 교훈은 같다 — 우리 SDCP 흡착에너지 8 회 반려 교훈 (`kb/methodology/estimand_before_running_2026_08_28.md`): **admissible state 가 여럿인데 선택 규칙이 없으면 스칼라 보고량은 정의되지 않는다.** BDTSRed 는 '중성 Li 결합형' 과 '이온화형' 둘 다 언급되고 (`Fig. S10`) 어느 상태의 E_b 인지 선언이 없다 |
| 관측창 | 미기재 | `D-2026-10-05-md-observation-window` — 짧은 MD 의 '없음' 서술에 관측창 한 줄 | 그들 AIMD: 기대 사건 1 ≈0.14 eV · 95 % 검출 ≈0.11 eV (§5.2 · 우리 산수) |
| 결합 자리 배위 | 기상 Li₂S₆ 클러스터 (Li 저배위) | `D-2026-10-05-adsorption-site-coordination` | 그들의 −1.7 ~ −2.45 eV 는 '저배위 Li 의 결합 포화' 로만 읽는다 |

### 7b. 개념 대조 — 우리 계와 닿는 곳
- **'준고체' 와 SE**: 이 논문의 QSSSR 은 액체 전해질 안의 조작적 정의 (LiPS 용해도 mM 수준 + 준이중 평탄 + 과충전 없음) 다. 전고체 Li–S (LPSCl 양극) 의 고체–고체 전환과 같은 말이 아니다 — 전고체에서는 '표면 국소 용매화' 를 해 줄 용매가 없고 그 역할을 혼합 전도체 · SE 자신의 산화환원이 맡는다 (`wang2025_miec…` · `cronk2026_lis_cathode…`). 우리 ESW 축 ① (S 기원 산화 개시) 과 겹치는 곳은 '반응하는 전해질' 이라는 생각뿐이다.
- **S₈ 다형 (α/β/γ)**: 재충전 황 상이 반응 경로 (용해–석출 / 준고체 / 매개) 의 지문으로 쓰인다는 점은 전고체 Li–S 양극 operando XRD 판독에 옮겨 쓸 수 있다 — 단 이 논문은 집합조직 · 정량 없이 '상 이름' 만 비교했다.
- **CIP · TFSI⁻ 우선 분해 → 무기 SEI**: argyrodite | Li 계면의 LiF · Li₂S 풍부 계면상 논의와 같은 언어지만 계가 다르다 (액체 SEI) — 수치 이식 금지.

### 7c. 🔑 층위를 갈라 쓴 결론 (원고 · 발표용 · 내부)
- 원고 · 발표에서 이 논문을 부를 때는 **"약용매화 액체 전해질에서 분자 첨가제로 준고체 황 반응을 가속한 사례"** 까지만 쓴다. '표면 국소 용매화' 는 저자의 해석으로 붙인다 (측정된 국소성이 아니다).
- 율 성능 숫자 (10 C · 16 C) 를 다른 셀과 견줄 때는 **방전 하한 전압 · 온도** 를 같이 적는다 — 없으면 쓰지 않는다.
- AIMD '3 배위 55 %' 는 계산 방법 사례 (표본 2 · 시작 구조 의존) 로만 인용한다.

## 8. DFT/계산 방법 ★ (템플릿 항목별 · 상세는 §4e)

| 항목 | 값 |
|---|---|
| 코드 | AIMD: 미기재 (PAW → VASP 로 보임) · 고전 MD: LAMMPS · 연속 용매화: Quantum ESPRESSO 7.2 + Environ 3.1 · 클러스터: 미기재 (B3LYP · IEFPCM → Gaussian 으로 보임) |
| 범함수 (+vdW) | AIMD PBE + DFT-D3 · 클러스터 B3LYP + D3(BJ) · Environ: 미기재 |
| pseudo / PAW / 기저 | AIMD PAW · Environ SG15 노름보존 · 클러스터 6-31+G(d,p) |
| k-points | AIMD Γ 만 · Environ 미기재 |
| ecut | AIMD 400 eV · Environ 60 Ry (본문 괄호 '780 eV' 는 오기 — 60 Ry ≈ 816 eV) |
| supercell / nat | AIMD 320–438 원자 (Li⁺ 2–6) · 고전 MD 3200–4380 원자 (Li⁺ 5–60 · 우리 역산) |
| DFT+U | 없음 |
| AIMD (ensemble/T/time) | NVT Nosé–Hoover · 303 K (한 런 400 K) · 평형 10 ps · 1 fs · 생산 미기재 |
| 고전 MD | NPT 1 ns → NVT 5 ns · 303 K · 1 fs · OPLS-AA (LigParGen) + 문헌 TFSI |
| MLIP | 없음 |
| 무질서 처리 | 액체 — 시작 구조 3 가지 (1 M CPME 만) · 시드 반복 없음 |
| 후처리 | RDF · 누적 CN (절단 반경 그림 점선 · 계마다 다름) · 배위수 분율 (프레임 무작위 추출) · ΔG_sol (Environ) · 결합에너지 E_b · LUMO 등고 · Mulliken 전하 · 시각화 (VESTA 류로 보임 · 미기재) |
| 기록 · 공개 | Source Data 제공 (zip — 이번엔 안 엶) · 힘장 매개변수 표 (`Table S6`–`S9`) · AIMD 입력 · 궤적 비공개 (영상 2 편만) |

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a–c | 개념도 — 용해–석출 (DOL/DME) vs 표면 국소 용매화 매개 QSSSR (CPME + BDTS) · 방전/충전 순환에서 PM⁻(sol) 이 Li₂Sₓ(s) 와 착물 → 용액 반응 → Li₂S/S₈ 에서 풀림 ('Loop') | '상 매개' 개념의 원전 그림 — 국소성은 측정이 아니라 가정이라는 점을 같이 단다 |
| 2a,b | Raman S–N–S (CPME ≈747 = 고체염 · DME ≈741 cm⁻¹) · ⁷Li NMR (CPME ≈ −0.79 · DME ≈ −1.16 ppm · FWHM 2.156 vs 1.206 Hz) | 약용매화 판정의 두 분광 지표 꼴 |
| 2c,d | AIMD Li–O g(r) · 누적 CN — CPME 3.43 (1.98 + 1.45) · DME 4.62 (3.00 + 1.62) · 절단 점선 ≈2.9 vs ≈3.3 Å | 계마다 절단 반경이 다른 CN 비교의 반례 |
| 2e | 배위 분율 — CPME 2/3/4 배위 1.2/55.2/43.6 % · DME 4/5/6 41.2/58.0/0.8 % | 표본 2 (Li⁺ 2 개) 의 분율 — 인용 금지 사례 |
| 2f,g | 대표 착물 구조 6 개 (Li–TFSI–CPME 3 배위 등) | 착물 명명 규약 참고 |
| 3a | GITT — DME 두 평탄 + 충전 셔틀 · CPME 준이중 평탄 ≈2.2 V | QSSSR 표지 |
| 3b | 0.2/0.1 C 100 cyc — CPME ≈1040 → ≈925 · DME · DOL/DME · LHCE 비교 | — |
| 3c,d | Li 증착 SEM (CPME 치밀 섬 · DME 느슨한 입자) | — |
| 3e | Li\|Li 600 h — CPME 과전압 ≈0.08 → ≈0.15 V 증가 · DME 300 h 뒤 출렁임 · y 축 범위 다름 | '안정' 서술과 과전압 증가의 어긋남 예 |
| 4a | BDTS 단독 vs S₈ 전압 곡선 — 첫 방전 1.5 V 활성화 · BDTS 가 S₈ 보다 먼저 환원 · 나중에 산화 | 매개자 전위 배치 판정 꼴 |
| 4b | UV–vis BDTSRed vs BDTSRed–Li₂S₆ (S₈ · S₆²⁻ · S₄²⁻ · S₈²⁻ 띠 · 사진) | 띠 겹침 · 흡광도 > 2 — 배정 신뢰 한계 |
| 4c | BDTS 환원 제안 — LUMO (C–S) · 라디칼 I/II → BDTSRed I (디티오카르바메이트) · II · 표면 결합 그림 | 분광 확인 없는 계산 기반 기전 사례 |
| 4d | BDTSRed–Li₂S₆ 결합에너지 I ≈ −1.9 · I′ ≈ −2.1 · II ≈ −1.7 · II′ ≈ −2.45 eV (figure-read) | 저배위 클러스터 결합 · 전하 상태 미선언 — 우리 보고량 규율의 반례 |
| 4e | S₈ 셀 0.1 C · 2 C (CPME vs BDTS) · 2 C 곡선이 ≈1.0 / ≈0.93 V 까지 · 충전 개시 장벽 삽입 ≈2.40 vs ≈2.30 V | 하한 전압이 1.2 V 아래로 내려간 비교 |
| 4f | 표면 국소 용매화 매개 QSSSR 개념도 | — |
| 5a,b | operando XRD 등고선 (방전 · 충전) — 캡션 'LiTFSI–CPME' · 그림은 α-S₈ 재생 (BDTS 쪽 서술과 맞음) | 캡션 ↔ 내용 불일치 예 |
| 5c | S₈ · Li₂S 정규화 세기 vs DOD/SOC (세 전해질) | 반응 경로 지문 (S₈ 소비 시점 · Li₂S 출현 시점) 판독 꼴 |
| 5d | 재충전 황 XRD — α (BDTS) · γ (CPME) · β (DME) · 처음 α | 재충전 다형 = 경로 지문 |
| 6a | 율 30 °C 0.1–10 C (하한 ≈1.2 → ≈0.5 V · 충전 ≈4.0 V 까지) | 하한 전압 불일치의 1 차 증거 |
| 6b | 율 55 °C 방전 0.2–16 C (1.0 V 까지) · 충전 0.5 C | — |
| 6c | 문헌 율 비교 (ref 11 · 24 · 55 · 61 · 66) | 조건 (하한 · 온도) 없는 비교 그림 |
| 6d–f | 장기 사이클 0.2/0.1 C 300 · 0.5/0.2 C 200 · 2/0.5 C 300 | 유지율 기준점 미기재 예 |
| ED1 | Extended Data Fig. 1 — 55 °C 용량 고정 희박 · 고부하 (a 2.0 mg · b 3.0 mg · c 5.1 mg) · d 40 °C 2.4 Ah 파우치 24 cyc | 용량 고정 사이클을 캡션에 밝힌 정직한 예 · 파우치 ≈69 % (figure-read) |
| S1 | Raman 맞춤 (CPME 단자리 31.6 / 두자리 68.4 % · DME SSIP 50 / 41 / 9 %) · LiTFSI 결정 · DME 착물 (안 봄) | — |
| S2 | AIMD 1/2/3 M CPME · 시작 구조 3 가지 · 배위 분율 표 | **시작 구조에 따라 종별 CN 분배가 뒤바뀐다** (a ↔ d) — 우리 '표본 · 시드' 규율의 근거 사례 |
| S3 | 3 · 4 배위 클러스터 (QE-Environ ΔG_sol) | ΔG_sol 부호의 오용 · Ry/Ha 환산 오류 예 |
| S4 | 고전 MD 0.25(라벨 0.5)–3 M · DME (안 봄) | AIMD ↔ 고전 MD CN 차 0.6–1.0 |
| S5 | 점도 · (THF)₃–LiTFSI AIMD (안 봄) | — |
| S6 | Li\|Cu CE · XPS · 70 일 EIS (안 봄) | — |
| S7 | BDTS CV · dQ/dV · S₈ CV (안 봄 · 인쇄 전위만 옮김) | BDTS 2.416/2.196/2.659 V · S₈ 2.132/1.820/2.494 V |
| S8 | BDTS 단독 율 · 1 C 사이클 (안 봄) | — |
| S9 | UV–vis — BDTS ≈ BDTSRed · 몰비 1:1–1:4 사진 · 24 h 변화 · S₈ · Li₂S 대조 | '환원체' 분광 확인 부재 · S₈ 대조의 작은 변화 |
| S10 | Mulliken 전하 변화 (라디칼 → BDTSRed) (안 봄) | — |
| S11 | 공명형 · BDTSRed I(meso)–Li₂S₆ · BDTSRed–Li₂S₄ 결합 (안 봄) | — |
| S12 | BDTS 셀 GITT · 1/2 사이클 (BDTS 환원 ≈2.45–2.5 V ≈50–60 mAh g⁻¹) | 첨가제 자체 용량 몫 산정 꼴 |
| S13 | S₈ LSV · Tafel (10 mV 창 · j₀ 2.2 vs 4.6 × 10⁻² mA cm⁻²) | 짧은 Tafel 창 · 원점 미정의 예 |
| S14 | Li₂S 첫 충전 (≈3.23 vs ≈3.72 V) · 반 방전 EIS (R2 ≈130 → ≈53 · R3 ≈172 → ≈151 Ω) | — |
| S15 | LiI 20/50 mM 대조 (55 °C) (안 봄) | — |
| S16 | 다른 SSE 에 BDTS (안 봄) | — |
| S17 | CPME operando XRD (γ-S₈) · 폭포 그림 (패널 라벨 'DME' ↔ 캡션 'CPME') · Li₂S (111) · 결정자 크기 | 라벨 불일치 · 측정 반복 n=5 를 오차막대로 쓴 예 |
| S18 | S K-edge XANES (안 봄) | LiPS ≈2470.7 · Li₂S ≈2476.2 eV |
| S19 | 55 °C 율 — BDTS 20/50/100 mM · CPME · LHCE · DOL/DME (하한 0.2–1.7 V 제각각) | **율 비교의 하한 전압 불일치 핵심 그림** |
| S20 | 5/0.2 C 100 cyc (안 봄) | — |
| S21 | 800 mAh g⁻¹ 고정 전압 곡선 (안 봄) | — |
| S22 | 용량 고정 없이 1.9–3 V 사이클 (안 봄) | 용량 고정 결과를 읽을 때 같이 봐야 할 그림 |
| S23 | 3 mg · E/S 5 / 5.1 mg · E/S 4 전압 곡선 (안 봄) | — |
| S24 | KB · 정렬 CNT · 활성탄 숙주 (안 봄) | — |
| Table S1 | 재충전 황 상 문헌 13 계 (캐솔라이트 β · QSSSR α 등) | 경로 ↔ 다형 대조표 |
| Table S2 | 문헌 율 성능 (숫자 열 글자층 누락) | — |
| Table S3 | 파우치 매개변수 (331 Wh kg⁻¹ · 2.4 Ah · N/P · 4 mg · 63.8 % · E/S 3 · 크기 · 층수 · 두께) | §3d 검산 |
| Table S4 | 파우치 질량 (6.21 · 6.00 · 3.36 · 15.57 g) | §3d 검산 |
| Table S5 | 용매 · 염 · 첨가제 단가 (숫자 글자층 누락) | — |
| Table S6 | 고전 MD LJ · 전하 (CPME 원자별 전하 포함) | — |
| Table S7 | 결합 매개변수 | — |
| Table S8 | 각 매개변수 | — |
| Table S9 | 이면각 매개변수 | — |

## 10. 비판 — 약한 곳 ★

**① 율 성능 비교의 방전 하한 전압 불일치 (가장 크다).** Methods 에 차단 전압이 없다. 그림에서 읽으면 BDTS 셀은 30 °C 10 C 를 ≈0.5 V (`Fig. 6a`) · 55 °C 10 C 를 ≈0.2 V (`Fig. S19f`) 까지 방전했고 충전은 ≈4.0 V 까지 올렸다. 같은 그림 묶음의 비교 셀은 BDTS 없는 CPME 1.0 V · LHCE ≈1.4 V · DOL/DME+LiNO₃ 1.5–1.7 V 다 (`Fig. S19c–e`). `Fig. 6c` 의 문헌 비교 셀 조건은 표시가 없다. 1.5 V 아래 용량은 Li₂S 를 넘어선 과방전 · 전해질 · 첨가제 (BDTS 활성화 1.44 V) 환원 몫이 섞일 수 있는 영역이다. "캐솔라이트 셀보다 율 성능이 낫다" (본문) 는 같은 하한에서는 성립하지 않는다 (figure-read · 10 C 곡선이 ≈1.5 V 에서 시작).

**② '표면 국소' 는 측정되지 않았다.** 국소성을 보일 공간 분해 측정 (operando 현미경 · 분리막 쪽 LiPS 정량 · 셔틀 전류 · 자가방전) 이 없다. 측정된 것은 벌크 용해도 ≈110 배 증가 (≈8 → ≈900 mM[S] · 우리 환산) 다. 기본 E/S 10 µL mg⁻¹ 에서는 S 의 ≈29 % 가 녹을 수 있다 (우리 산수 · 논문은 E/S 5 를 가정해 15 %). 첫 평탄 S₈ 소비가 DME 캐솔라이트와 같은 속도라는 `Fig. 5c` 는 오히려 '전역 부분 용해' 쪽 그림과 잘 맞는다. 셔틀 전류 (이 그룹 후속 `shen2026` 은 쟀다) 가 BDTS 셀에는 없다.

**③ BDTSRed 의 정체가 분광으로 확인되지 않았다.** C–S 절단은 LUMO 위치에서 추론했을 뿐이고, BDTS 와 BDTSRed 의 UV–vis 가 거의 같다 (`Fig. S9a` · 저자 인정). 환원 생성물의 ¹H/¹³C NMR · MS · IR 이 없다. BDTSRed 를 LSV 로 '전기환원' 해 만든 용액이 얼마나 환원됐는지 (전하량 · 수율) 도 적혀 있지 않다.

**④ '상 매개 ≠ 산화환원 매개' 를 배제하지 못했다.** BDTS 는 2.42 · 2.20 V 환원 · 2.66 V 산화하는 산화환원 활성 분자다 (`Fig. S7c`). 충전 때 생기는 산화형 BDTS 가 Li₂S/LiPS 를 화학 산화하는 고전 RM 경로가 열역학적으로 열려 있다 (우리 추론). `Fig. S14a` 의 Li₂S 장벽 감소 (3.72 → 3.23 V) 앞에 ≈2.5 V BDTSRed 산화 계단이 먼저 지나간다. 배제 시험은 다른 분자 (LiI) 하나와의 성능 비교뿐이다 — 같은 분자에서 착물화만 끄는 대조 (예: Li 결합 자리를 막은 유사체) 가 필요했다.

**⑤ 연속 용매화 ΔG_sol 의 부호로 '존재' 를 판정했다.** 극성 클러스터를 ε 4.76 연속체에 넣으면 ΔG_sol 은 거의 늘 음수다. 3 배위 대 4 배위의 상대 안정성은 Li–TFSI–CPME + CPME → Li–TFSI–2CPME 반응 자유에너지 (같은 연속체 · 열 보정) 로 물어야 한다. 저자 스스로 "절대값은 구조 비교에 못 쓴다" 고 적어 놓고 결론에 썼다.

**⑥ 단위 환산 오류.** `Fig. S3` 논의의 −0.0453 Ry = −14.2 kcal/mol 인데 −28.4814 kcal/mol 로 적었다 (Hartree 환산값). −0.0188 Ry 도 같은 꼴 (−5.9 → '−11.85'). Environ SI 의 ecutwfc "60 Ryd (780 eV)" 도 60 Ry = 816 eV 다.

**⑦ AIMD 통계 · 보고.** Li⁺ 2 개 · 생산 길이 미기재 · 시드 1. 시작 구조를 바꾸면 총 CN 은 같아도 **종별 분배 (CPME ↔ TFSI⁻) 가 뒤바뀐다** (`Fig. S2a` vs `S2d` · figure-read). 하나는 400 K 로 돌렸다. 절단 반경이 CPME ≈2.9 · DME ≈3.3 Å 로 계마다 다르다. 1 M 상자의 실제 농도는 ≈0.81 M · '3 M' 상자는 ≈2.03 M 이다 (우리 산수). 고전 MD 와 0.6–1.0 차이 나는 CN 을 "고전 MD 과대평가" 로 정리했는데, 같은 크기의 대안 (AIMD 통계 부족) 을 시험하지 않았다. 고전 MD 최저 농도는 Methods '0.25 M' · 그림 '0.5 M'.

**⑧ 클러스터 결합에너지의 보고량이 정의되지 않았다.** BDTSRed 의 전하 상태 (Li 결합 중성 · 이온화형) 가 둘 다 언급되는데 어느 쪽인지 선언이 없고, BSSE · ΔG · 경쟁 리간드 (CPME · TFSI⁻) 결합 기준이 없다. 결합 상대가 기상 저배위 Li₂S₆ 라 '고체 표면 착물화' 를 대변하지 않는다. Methods 의 "AIMD 에서 시작 구조를 가져왔다" 는 AIMD 상자에 BDTS 가 없어 앞뒤가 안 맞는다.

**⑨ '안정' 서술이 그림보다 강하다.** Li\|Li 과전압이 600 h 에 ≈두 배 (≈0.08 → ≈0.15 V) 로 늘었는데 "steady" (`Fig. 3e`) · 2 C 사이클은 첫 15 cyc 에 ≈1/3 을 잃었는데 "very stable" (`Fig. 6f`) · 파우치 24 cyc ≈69 % 인데 "steady" (Extended Data Fig. 1d) · 유지율 90 % · 95 % 의 기준 사이클 미기재.

**⑩ 그림 캡션과 패널 라벨 불일치.** `Fig. 5a,b` 캡션 'LiTFSI–CPME' ↔ 내용 (α-S₈ 재생 · 짧은 시간 축) 은 BDTS 셀 서술과 맞는다 · `Fig. S17b,c` 패널 'LiTFSI-DME' ↔ 캡션 'LiTFSI-CPME' (γ-S₈) · 본문이 UV–vis 를 'Fig. 4c' 로 가리킨다 (실제 4b) · SI 가 두 번째 시작 구조 런도 'Fig. 2d' 로 가리킨다 (실제 2e) · Raman 띠를 'nm' 로 적었다.

**⑪ '착물화가 매우 빠르다' 의 근거가 약하다.** 1.38 × 10⁻⁵ mol L⁻¹ s⁻¹ 은 고체 분말 용해를 육안 끝점으로 잰 값이고, 환산하면 ≈1 h 다 (우리 산수) — 2 C · 10 C 방전보다 길다. 반응 앞면의 착물화 속도를 대변하지 못한다.

**⑫ Tafel 맞춤.** 10 mV 창 · 과전압 원점 미정의 · BDTS 자기 환원 봉우리 (2.196 V) 가 같은 창에 걸림 — 교환 전류 '2 배' 를 BDTS 의 S₈ 촉진으로 귀속할 수 없다.

**⑬ 첨가제 자체 용량.** 50 mM BDTS 는 S 기준 ≈27 mAh g⁻¹ (2 e⁻ · E/S 10 · 우리 산수) · 그림상 ≈50–60 mAh g⁻¹ (`Fig. S12b`) 를 낸다. 고율 용량의 수 % – 10 % 가 S 가 아닌 BDTS 몫일 수 있는데, 성능 표에서 빼지 않았다.

**⑭ 온도가 섞였다.** 기본 30 °C · 율 최고치 · LiI 대조 · 희박 시험 55 °C · 파우치 40 °C. 같은 조건의 대조가 없는 그림이 많다 (예: 파우치 BDTS 없는 셀은 있지만 희박 용량 고정 시험의 BDTS 없는 대조는 없다).

**⑮ 반복 수.** 대부분 그림이 셀 1 개 · 결정자 크기 오차막대는 같은 셀의 연속 XRD 5 장.

**좋은 점 (공정하게)**: 기여 진술에 계산 담당을 적었다 · 힘장 매개변수 전체를 표로 냈다 · AIMD 시작 구조 의존을 스스로 시험했다 (결론은 과했지만) · 희박 시험이 용량 고정이라는 사실을 캡션에 밝혔다 · 포장 포함 비에너지와 질량 표를 같이 냈다 (검산 가능) · 문헌 재충전 황 상 표 (`Table S1`) 는 쓸모 있다.

## 11. 적용 인사이트 ★ (우리 연구에 어떻게)
1. **MD 통계 규율의 외부 반례로 쓴다.** Li⁺ 2 개 · 단일 시드 AIMD 에서 '배위 분율 55 %' 가 나왔고, 시작 구조를 바꾸자 종별 분배가 뒤바뀌었다 — 우리 '비율은 멀티시드 판정만' · 관측창 한 줄 규율이 왜 있는지 설명할 때 이 그림 (`Fig. S2a,d`) 이 좋다.
2. **분자 결합에너지 보고량 카드의 체크리스트.** 전하 상태 선언 · 경쟁 리간드 기준 · BSSE · 저배위 결합 자리 표시 — 이 논문이 빠뜨린 넷이 우리 SDCP 카드 교훈과 같다 (§7a).
3. **율 · 용량 비교에서 하한 전압 · 온도를 먼저 맞춘다.** 문헌 성능 수치를 우리 원고 · 발표에 옮길 때 '같은 하한 · 같은 온도' 가 아니면 비교 그림에 넣지 않는다.
4. **재충전 황 다형을 경로 지문으로** — 전고체 Li–S operando XRD 를 읽을 일이 생기면 `Table S1` (캐솔라이트 β / QSSSR α / 이 논문 γ) 이 출발점이다 (집합조직 · 정량은 우리가 보태야 한다).

## 12. 인용 가능 문장 (영문 초안 · 랩 표기 *Nat. Chem.*, 17, 614 (2025))

- A weakly solvating ether electrolyte (1 M LiTFSI in cyclopentyl methyl ether) restricts Li₂S₆ solubility to the millimolar level and supports a quasi-solid-state sulfur reaction, and a dithiocarbamate-forming additive accelerates this reaction by increasing polysulfide solubility (*Nat. Chem.*, 17, 614 (2025)).
- In that work, the surface localization of the solvated polysulfides is a proposed mechanism; the measured quantities are bulk solubility, voltage profiles, and operando diffraction.
- ⚠ 율 성능 수치 (10 C 583 · 16 C 494 mAh g⁻¹) 를 인용하면 **"discharged to ≈0.5 V (30 °C) or 1.0 V (55 °C)"** 를 같이 쓴다 — 하한 전압 없이 인용하지 않는다.
- ⚠ AIMD '3 배위 Li⁺' 는 "in two-Li⁺ AIMD cells" 를 붙여서만 쓴다.

## 13. 주의 / 한계 (인용 규율)
- 액체 전해질 문헌이다 — 우리 SE 물성 (σ · Ea · ESW · 기계 · gap) 과 **같은 표에 놓지 않는다**. 이 논문의 'QSSSR' 은 액체 안의 조작적 정의 (LiPS 용해도 mM 수준 + 준이중 평탄 + 과충전 없음) 다.
- 그림에서만 읽은 값 (`figure-read ≈`) 은 원고 인용 금지 — 경향 서술에만.
- '표면 국소 용매화' · '상 매개 ≠ RM' 은 저자 해석으로만 붙인다.
- 계산값 (CN · ΔG_sol · E_b) 은 방법 (상자 · 시드 · 기준 상태) 을 같이 적지 않으면 인용하지 않는다 · ΔG_sol 의 kcal 값은 단위 오류가 있다 (§10-⑥).
- 이 digest 는 Source Data zip · 영상 · 안 본 SI 그림 16 장의 내용을 확인하지 않았다 (§0).

## 14. 이어 읽기 — litdb 의 관련 digest

| digest | 이 논문과 닿는 곳 | 같이 읽을 때 |
|---|---|---|
| `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` | **같은 그룹 · 같은 CPME 바탕** — 매개자 분자 대신 THF 공용매로 같은 '표면 국소 용매화' 를 노린 후속. 이 논문을 계보에서 'Liu 2025 *Nat. Chem.* (ref 26)' 로 부른다 | 이 논문에 없는 **셔틀 전류** · PITT 핵생성 판정 · β-S₈ 면 흡착 DFT 가 거기 있다. 거기 digest 는 Li₂S₆ 합성 '8:3' 을 S 원자 기준으로 읽어 Li₂S₅.₃ 이라 적었는데, 이 논문 Methods ("lithium borohydride and sulfur (S₈) by a molar ratio of 8:3") 기준이면 Li : S₈ = 8 : 3 → Li₂S₆ 로 맞는다 (원문 표현이 다를 수 있어 그쪽 digest 는 고치지 않았다) · 파우치 설계 (68 × 96 mm · N/P 1.87) 가 같다 |
| `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` | 같은 그룹 (교신 Yatao Liu) · 약용매화 용매 (실록산 FPDS) + 분자 매개자 (DIP) 를 한 전해질에 합친 판 | 매개자 쪽 증거 (셔틀 · 자가방전 측정 여부) 를 이 논문과 나란히 놓고 '상 매개' 가 계열 안에서 어떻게 검증됐는지 본다 |
| `lai2026_mtbe_moderately_solvating_ether_cosolvent_lis` | CPME 를 포함한 단일 산소 에테르 넷을 DOL/DME 에 30 vol% 섞은 '중간 용매화' 전해질 · 그 `Table S2` 가 이 논문 (BDTS–LiTFSI–CPME) 을 비교 행으로 인용 | 약용매화 (이 논문) ↔ 중간 용매화 (lai) 의 경계 — 이 논문의 BDTS 셀이 실제로는 중간 용해도 쪽에 가 있을 수 있다는 §10-② 판단과 같이 읽는다 |
| `peng2026_er_dn_solvent_screening_csa_methf_lis` | ε–DN 지도에서 용매를 다섯 영역으로 나눔 | CPME (ε 4.76) 의 자리를 지도에서 확인 |
| `wei2026_data_driven_hea_mediator_lis` | 액체 Li–S '매개자' (고체 HEA 중간층) · 흡착 DFT | 분자 매개자 (이 논문) ↔ 고체 촉매 매개자 · 계산 보고 항목 대조 |
| `guan2026_feco_vs_in2s3_li2s_electrocrystallization` | Li₂S 전기결정화 · 결정자 크기 · 핵생성 | 이 논문의 'Li₂S 가 늦게 · 작게' 판독을 핵생성 판정 (Scharifker–Hills) 쪽과 견준다 |
| `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` | argyrodite 분리막 + 액체 전해질 준고체 Li–S · 에테르 쪽 계면상 성장 | 이 논문 계열 전해질이 argyrodite 와 만나면 무엇이 생기는지 — 우리 SE 와 액체 Li–S 의 다리 |
| `yu2025_cng_host_suppress_argyrodite_oxidation_lis` | 전고체 Li–S 에서 숙주가 argyrodite 산화를 줄임 | 액체에선 '매개자' 가 하는 일을 전고체에선 숙주 · SE 가 맡는다 |
| `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` | 전고체 Li–S 삼상 계면 · AIMD | 용매 없는 '표면 반응' 의 대응물 · AIMD 보고 항목 비교 |
| `cronk2026_lis_cathode_interphase_chemistry` | LPSCl 촉매전해질 · 전고체 양극 계면상 | 전고체에서 '반응하는 전해질' 은 SE 자신 (우리 축 ①) |
| `cronk2026_lis_positive_electrode_geometry_fem` | 전고체 Li–S 양극 기하 · 활성 표면 | '표면 부동태 → 활성 표면 유지' 개념의 전고체판 |
| `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` | 전고체 Li–S 반응 기전 지도 | 액체 → 준고체 (이 논문) → 전고체 의 사다리 |

## 15. 기법 용어 미니사전

- **WSE · SSE** — 약용매화 전해질 (weakly solvating) · 폴리설파이드를 거의 안 녹이는 전해질 (sparingly solvating). 이 논문에서 둘은 거의 같은 뜻으로 쓰인다.
- **QSSSR (quasi-solid-state sulfur reaction)** — LiPS 가 크게 녹지 않은 채 S₈ → Li₂S 가 고체 (준고체) 상태로 진행하는 경로. 표지: 준이중 방전 평탄 (≈2.2 V) · 과충전 없음.
- **상 매개자 (phase mediator, PM)** — 저자 용어. 고체 LiPS 와 착물을 만들어 표면 근처에서 용액상으로 옮겨 주고, 생성물 (Li₂S · S₈) 에서는 풀려나는 분자. 산화환원 매개자 (RM) 는 자신이 먼저 산화/환원된 뒤 전자를 고체에 주고받는 분자 — 둘의 경계는 이 논문에서 실험으로 갈리지 않았다.
- **BDTS · BDTSRed** — bis(dimethylthiocarbamyl) sulfide (테트라메틸티우람 모노설파이드 · 우리 식별) · 그 환원체 (제안: 디티오카르바메이트 Me₂NCS₂⁻ 와 티오카르바모일 조각).
- **디티오카르바메이트** — R₂N–CS₂⁻. 두 S 로 금속을 킬레이트하는 리간드. 공명형 티오우레이드 (R₂N⁺=CS₂²⁻) 로 N 이 전자 부족 · S 가 전자 풍부.
- **CIP · SSIP · AGG** — 접촉 이온쌍 (단자리 · 두자리) · 용매 분리 이온쌍 · 응집체 (TFSI⁻ S–N–S Raman 띠로 가름).
- **LHCE** — 국소 고농도 전해질 (농후 염–용매 착물을 비용매 희석제로 묽힌 것). 밀도 · 점도 · 값이 높다는 것이 이 논문의 비교 논지.
- **RDF g(r) · 누적 CN · 절단 반경** — 동경 분포 함수 · 그 적분 배위수 · 첫 껍질을 끊는 거리 (보통 g(r) 첫 극소). 계마다 다른 절단 반경을 쓰면 CN 비교가 흔들린다.
- **AIMD vs 고전 MD** — DFT 힘 (짧고 작다 · 수십 ps · 수백 원자) vs 힘장 (길고 크다 · ns · 수천 원자). 용매화 CN 이 둘 사이에서 자주 어긋난다.
- **연속 용매 모형 (SCCS · IEFPCM)** — 용매를 유전 연속체로 바꿔 넣는 방법. ΔG_sol = E(용매) − E(진공) 은 극성 용질이면 거의 늘 음수 — 구조 간 상대 안정성은 같은 모형 안 반응 에너지로 묻는다.
- **BSSE** — 유한 기저에서 짝 분자의 기저를 빌려 결합이 과대평가되는 오차 (counterpoise 로 보정).
- **Mulliken 전하** — 기저 함수에 따라 크게 바뀌는 원자 전하 분할법 (경향만).
- **LUMO** — 최저 비점유 분자 궤도. 첫 전자가 들어갈 자리 — 결합 절단 위치 추론에 쓰지만 생성물 확인을 대신하지 못한다.
- **GITT** — 정전류 펄스 + 휴지로 준평형 전압을 보는 법.
- **Tafel · 교환 전류 밀도 j₀** — 과전압–log 전류 직선의 기울기와 η = 0 외삽 절편. 직선 구간이 충분히 넓고 과전압 원점이 정의돼야 한다.
- **operando XRD 정규화 세기** — 한 상의 최대 세기를 100 % 로 둔 상대 추이. 셀 사이 절대량 비교는 안 된다.
- **α · β · γ-S₈** — 사방정 (실온 안정) · 단사정 (고온 · 준안정) · 단사정 (자개 모양 · 용액/용융물에서) 황. 재충전 상이 반응 경로 지문으로 쓰인다.
- **Scherrer 결정자 크기** — 회절 봉우리 폭에서 낸 결맞음 길이. 기기 퍼짐 보정이 필요하다.
- **S K-edge XANES** — 황 1s 흡수 가장자리. LiPS 말단 S 전가장자리 (≈2470.7 eV) · S–S (≈2472.3) · Li₂S (≈2476.2) · TFSI⁻ 술포닐 (≈2480 · ≈2485 eV) — 이 논문 값.
- **E/S ratio · N/P** — 전해액 부피 (µL) / 황 질량 (mg) · 음극 (Li) 용량 / 양극 (S) 용량.
- **용량 고정 사이클** — 방전을 정해진 용량 (예: 800 mAh g⁻¹) 에서 끊는 시험. 용량 감쇠가 그림에 안 나타나고, 대신 끝 전압이 내려간다 — 결과는 고정 없는 시험과 같이 읽는다.

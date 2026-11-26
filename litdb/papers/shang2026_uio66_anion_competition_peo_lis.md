<!-- digest 초판 2026-11-26 (논문 에이전트 · 범위 제한 세션: digest 파일 + 그림 폴더만 씀 —
     INDEX.md · comparison_vs_ours.md · _sources.json · pdf_map.tsv 반영과 커밋은 부모 세션 몫).
     ① 그림 추출: tools/litdb/extract_figures.py 의 extract() 를 직접 불러 이 논문 폴더에만 썼다 (CLI 는 끝에 공유 색인
        litdb/figures/_sources.json 을 다시 쓰므로 피했다 · 실행 전후 _sources.json · pdf_map.tsv md5 동일 확인).
        26장 = 본문 Fig. 1–7 + SI Fig. S1–S17 + Table S1–S2. 번호 공백 경고 없음.
     ② 실제로 본 그림 (원본 크기 Read): `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` · `Fig. 7` · `Fig. S16` (7장).
        안 본 그림: `Fig. 1` (합성 모식도 · XRD · BET · TEM · SEM · EDS) · `Fig. S1`–`S15` · `Fig. S17` — 캡션과 본문 서술만 썼다.
        표 `Table S1` · `Table S2` 는 PDF 텍스트로 읽었다 (이미지 안 봄).
     ③ 우리 산수: Table S1 → 아레니우스 재적합 · Table S2 → 결합에너지 재계산 · Tafel 기울기 → αn · 홉 수 검산 · TGA 잔량 질량수지.
     ④ 홉 수 검산 = D-2026-09-27-barrier-hop-count (ν₀ 10¹³ s⁻¹ 가정 · T 명시).
     ⑤ 흡착 자리 배위 = D-2026-10-05-adsorption-site-coordination (구조 비공개 → '배위 미확인' 병기). -->

# Dynamic anion competition induced charge reconstruction toward accelerated ion migration and sulfur conversion kinetics in solid-state lithium–sulfur batteries — Shang et al. (*Chem. Eng. J.* 2026, Journal Pre-proof)

> slug `shang2026_uio66_anion_competition_peo_lis` · DOI `10.1016/j.cej.2026.184621` (CEJ 184621 · PII S1385-8947(26)12091-9) · type `exp (PEO/LiTFSI + PAN/UiO-66 전기방사 섬유망 복합 고분자전해질 · EIS · LSV · t⁺ · 대칭셀 · CV/Tafel · in-situ EIS/DRT · GITT · XPS/VB-XPS · FTIR/Raman · UV-vis) + DFT 보조 (CP2K PBE-D3(BJ) · 고립 Zr₆ 노드 클러스터 · 결합에너지 2개 + CDD · Bader · ELF · DOS/PDOS)` · PDF `litdb/inbox/1. Dynamic anion competition … batteries.pdf` (본문 28 pp, Journal Pre-proof) + `litdb/inbox/1. Sup) Dynamic anion competition … batteries.pdf` (SI 30 pp: 실험 pp.2–7 · DFT pp.7–8 · `Fig. S1`–`S17` · `Table S1`–`S2`) · digested `2026-11-26` · status ✅ · 태그 **[외부 · 고분자 전해질 · Li–S]**

> elements: Zr, S, Li, O, N, F, C
> methods: DFT, Bader, ELF, DOS, PDOS, XPS, Raman, ESW

> **저자**: **Hongyu Shang**ᵃ · **Rong Yang**ᵃ\* (yangrong@xaut.edu.cn) · Yurou Wangᵃ · Zhixin Muᵃ · Xin Dongᵃ · Ruixuan Yangᵃ · Ying Zhuᵇ · Min Zhangᵃ · **Jou-Hyeon Ahn**ᶜ · Hyun Woo Kimᶜ — ᵃ西安理工大学(Xi'an Univ. of Technology) 재료과학공학원 · ᵇ같은 대학 인문외국어학원 · ᶜ**경상국립대(Gyeongsang National Univ.)** 재료공학·융합기술학과.
> 접수 2026-08-29 · 수정 2026-10-23 · 수락 2026-11-22 · **Journal Pre-proof** (최종 편집본 아님 — 인용 시 지위를 밝힌다). 자금: NSFC 52571179 · Energy Shaanxi Lab ESL B/202423 · 陕西 2023GHJD-18 · 咸阳 L2025-ZDYF-XCL-011 · 한국 과기정통부/연구개발특구진흥재단 RS-2023-IN231026. **데이터: "요청 시 제공"** — DFT 구조 비공개.
> 기여: 계산(Software/Methodology) = **Ruixuan Yang · Min Zhang**. 같은 그룹 선행: ref [12] Shang *et al.* *Energy Storage Mater.* 89 (2026) 105199 (초분자 host–guest · 고체 Li–S).

> **트랙 판정 (정직하게)**: 재료가 **PEO-LiTFSI 고분자 전해질 + MOF 충전재**이고 전지는 **Li–S (S/CNT 양극 · 60 °C)** 다. 우리 계(argyrodite 황화물 LPSCl · QE PBE · UMA MD)와 **겹치는 물성 칸이 없다.** DFT 는 *전하를 띤 고립 클러스터* 위 결합에너지 2개 + 그림 분석 묶음이다 ⇒ **A–D 물성 4축 표에는 넣지 않는다.** 쓸모는 ① 화학결합 규모 흡착에너지의 **방법 반례**(전하 상태가 다른 두 흡착종 비교 — 저자 스스로 과대평가를 인정) ② CP2K 설정 선례 하나 ③ Li–S 양극 쪽 S 2p XPS 지정의 **경고 사례**.

> **관련 digest**: 고분자 전해질 + '화학결합 규모 흡착에너지' 반례 계열 `[Yuan26LCE]` `yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal` (SiO₂–TFSI⁻ 3.11 eV · 1-배위 Si) · `[Yu26Pol]` `yu2026_pvdf_mos2_anion_solvent_confinement` · `[Meng26LZF]` `meng2026_pvdf_li2zrf6_phase_ordering` (FSI⁻/LZF) · CP2K 선례 `[Liu26CCTO]` `liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl` · `[Zhang26PI3]` `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector` · Li–S 쪽 `cronk2026_lis_cathode_interphase_chemistry` · `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` · `luo2026_lis_separator_crystal_engineering_review`.

> **본 digest 에서 실제로 본 그림 (2026-11-26)**: `Fig. 2` (DFT 전부) · `Fig. 3` (UV-vis · XPS · VB-XPS · 모식도) · `Fig. 4` (XRD · TGA · 인장 · FTIR · Raman) · `Fig. 5` (σ · 아레니우스 · LSV · t⁺ · 대칭셀) · `Fig. 6` (CV · Tafel · in-situ EIS · DRT) · `Fig. 7` (GITT · 사이클 · LFP · 파우치) · `Fig. S16` (ex-situ S 2p) — **7장, 원본 크기**. **안 본 그림**: `Fig. 1` · `Fig. S1`–`S15` · `Fig. S17` (캡션·본문만 사용). `Table S1`·`S2` 는 PDF 텍스트.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문에 없는 우리 계산은 **(우리 산수)** 로 표시했다. 문헌 수치는 소환값이다 — 우리 db 절대값과 섞지 않는다.

---

## 0. 이 digest 를 읽는 법 — 판정 먼저

주장 (한 문장): *"UiO-66 의 열린 Zr⁴⁺ 자리가 처음엔 TFSI⁻ 를 약하게 잡아 LiTFSI 해리·Li⁺ 이동을 돕고, 방전 중 생긴 폴리설파이드(Sₙ²⁻)가 더 세게 붙어 TFSI⁻ 를 밀어내며 Zr 자리 전하를 재구성해 황 변환을 빠르게 한다."*

| 질문 | 한 줄 답 | 절 |
|---|---|---|
| ① σ 2.8 배 향상이 UiO-66(Zr⁴⁺) 덕인가 | **60 °C 에서는 거의 아니다.** 같은 `Table S1` 에 UiO-66 **없는** PAN 섬유망 대조(PPL)가 있고, 60 °C σ 는 PPL **3.54** vs PUPL **3.75 ×10⁻⁴ S cm⁻¹** — UiO-66 몫 ≈ **1.06 배** (우리 산수). 2.8 배 중 대부분은 PAN 섬유망이다. UiO-66 효과가 큰 곳은 **25 °C (PPL 대비 4.4 배)** — 결정화 억제 영역 | §3a · §10-① |
| ② DFT 가 "S₆²⁻ 가 TFSI⁻ 보다 세게 붙는다"를 보였나 | **보이지 못한다.** 클러스터 전하 **+4**, 흡착종 전하 **−1 vs −2** 라 −11.96 vs −26.45 eV 의 차이는 **쿨롱 항**이 대부분이고, 저자도 SI 에서 그렇게 인정한다. 구조 비공개 → 결합 자리 배위 미확인 | §4 · §10-② |
| ③ 그림이 본문 서술을 받쳐 주나 | **여러 곳에서 어긋난다** — ELF 단면(`Fig. 2h,i`)엔 흡착종이 안 보이고, `Fig. 3d` 의 폴리설파이드 S 2p 를 169–171 eV(설페이트 대역)에 지정, `Fig. S16` 의 "Briding S" 는 본문이 말한 163.5 eV 가 아니라 ≈167–168 eV, Tafel 기울기 15 mV dec⁻¹ 는 αn ≈ 4.3 (비물리), DRT 의 가장 센 봉우리(10–100 s)는 저자의 τ 구간 정의 밖 | §5 · §10-③ |
| ④ "고체" Li–S 인가 | **아니다 — 혼성이다.** SI 1.6: S 양극에 **액체 전해액 5 µL** (1 M LiTFSI DOL/DME + 2 wt% LiNO₃) 를 적셔 조립. LFP 셀만 액체 0 | §2 · §10-④ |
| ⑤ 우리 일에 쓸 것 | 방법 반례 1건(전하 다른 흡착종 결합에너지 비교 금지) + CP2K 설정 1점. 물성 비교값 없음 | §7 · §8 |

---

## 1. 한 줄 요약

PAN/UiO-66 전기방사 섬유망(PU)에 PEO/LiTFSI(PL)를 함침한 복합 고분자 전해질 **PUPL** 로 60 °C 고체(실제로는 양극 액체 젖음) Li–S 전지를 만들고, 성능 향상을 *"TFSI⁻ → Sₙ²⁻ 음이온 경쟁 배위에 의한 Zr⁴⁺ 루이스산 자리의 동적 전하 재구성"* 으로 설명한다. 전기화학 지표(σ 3.75×10⁻⁴ S cm⁻¹ @60 °C · t⁺ 0.65 · 1600 h 대칭셀 · 초기 1282.81 mAh g⁻¹)는 실측이지만, **기전 귀속은 대조군·그림·계산 모형이 받쳐 주지 못한다.**

## 2. 메타

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| H. Shang, R. Yang\* 외 (XAUT · 경상국립대 J.-H. Ahn) | *Chem. Eng. J.* 2026 (Journal Pre-proof, CEJ 184621) | 10.1016/j.cej.2026.184621 | PEO (Mw 6×10⁵) 1.20 g + LiTFSI 0.52 g (PL) · PAN/UiO-66 섬유막 (UiO-66 : PAN = 5 / **7.5** / 10 wt%) · PUPL-7.5 질량분율 **PL 91.05 · PAN 8.28 · UiO-66 0.67 wt%** (SI 1.3) · 막 두께 ≈158 µm · PU 막 ≈2 µm · 섬유 지름 ≈0.40 µm · UiO-66 ≈150 nm 팔면체 · BET 961.60 m² g⁻¹ | exp 주 + DFT 보조 |

- 셀: Li | 전해질 | S (S/CNT 6:4 → 155 °C 12 h · 양극 S/CNT : CNT : PVDF = 7:2:1 · **S 1.0 mg cm⁻²** · ⌀12.5 mm) · **양극에만 액체 5 µL** · 1.7–2.8 V · **모든 전기화학 60 °C**. Li | PUPL | LFP (액체 없음). 굽힘·절단 파우치 LED 시연 (`Fig. 7h` — "room temperature").
- EO:Li 비 (우리 산수): PEO 1.20 g / 44.05 = 27.2 mmol EO · LiTFSI 0.52 g / 287.1 = 1.81 mmol → **EO:Li ≈ 15**.

## 3. 핵심 물성 (수치) — 전부 소환값

### 3a. 이온 수송 (`Fig. 5`, `Table S1`, `Fig. S7`–`S11`)

| 물성 | PL | PPL (PAN, UiO-66 없음) | PUPL-5 | **PUPL (7.5)** | PUPL-10 | 비고 |
|---|---|---|---|---|---|---|
| σ 25 °C (S cm⁻¹) | 1.48×10⁻⁶ | 8.84×10⁻⁶ | 8.29×10⁻⁶ | **3.92×10⁻⁵** | 2.18×10⁻⁵ | `Table S1` |
| σ 60 °C | 1.30×10⁻⁴ | **3.54×10⁻⁴** | 2.99×10⁻⁴ | **3.75×10⁻⁴** | 2.18×10⁻⁴ | 본문 "≈2.8 배 vs PL" |
| σ 80 °C | 4.49×10⁻⁴ | 7.51×10⁻⁴ | 6.74×10⁻⁴ | 7.57×10⁻⁴ | 5.16×10⁻⁴ | |
| Ea 저온 (25–50 °C) | **1.15 eV** | 1.04 | 1.03 | **0.64** | 0.52 | 구간 아레니우스 (`Fig. 5c`, `S10`, `S11`) |
| Ea 고온 (60–80 °C) | 0.62 | 0.39 | 0.41 | **0.35** | 0.44 | |
| t⁺ (Bruce–Vincent) | 0.21 | n/a | n/a | **0.65** | n/a | `Fig. 5e,f` · ΔV 미기재 |
| LSV 산화 개시 | 3.90 V | n/a | 4.69 V | **5.15 V** | 4.91 V | `Fig. 5d`, `S12` · 접선 외삽 · 0.1 mV s⁻¹ · 60 °C |
| Li\|Li 0.1 mA cm⁻² | ≈330 h 단락 | n/a | n/a | **>1600 h** | n/a | `Fig. 5g` |
| 율속 대칭셀 | 0.20 mA cm⁻² 에서 단락 | | | 0.30 mA cm⁻² 까지 안정 | | `Fig. 5h,i` |

**우리 재적합 (Table S1 → ln σ vs 1/T 최소자승, 우리 산수)**: PL 1.16 / 0.62 · PPL 1.03 / 0.38 · PUPL-5 1.03 / 0.41 · PUPL 0.65 / 0.36 · PUPL-10 0.52 / 0.44 eV — 논문 값과 ±0.01 eV 로 **재현된다**. 60 °C 를 고온 구간에 넣은 분할이다 (`Fig. 5c` 에서 확인: 고온 3점 = 1000/T 2.83–3.00, 저온 4점 = 3.10–3.36).

**대조군 비율 (우리 산수)**: PUPL/PPL = 25 °C **4.43 배** · 60 °C **1.06 배** · 80 °C **1.01 배**. PPL/PL @60 °C = 2.72 배. ⇒ *"2.8 배"* 의 거의 전부가 PAN 섬유망 몫이다.

⚠ `Table S1` 이상점: PL 60 °C 1.30×10⁻⁴ ≈ 70 °C 1.31×10⁻⁴ (10 K 동안 평탄) · PUPL-10 25 °C 와 60 °C 가 가수 2.18 로 같다 — 전사 오류 가능성. 원자료 비공개라 확인 불가.

### 3b. 황 변환·전지 (`Fig. 6`, `Fig. 7`)

| 물성 | PL | PUPL | 비고 |
|---|---|---|---|
| CV ΔE (0.1 mV s⁻¹) | 0.42 V | **0.38 V** | `Fig. 6c` |
| Tafel (`Fig. 6d` "Peak B") | 33.36 mV dec⁻¹ | **15.45** | 본문: 환원 |
| Tafel (`Fig. 6e` "Peak C") | 39.35 mV dec⁻¹ | **16.75** | 본문: 산화 |
| GITT 평균 D_Li⁺ | 1.33×10⁻¹³ cm² s⁻¹ | **1.34×10⁻¹²** | `Fig. 7a` · **양극 겉보기 D** (SI 식 4: 활물질 m_B·V_M·M_B 사용) |
| 초기 방전용량 0.1 C | 867.60 mAh g⁻¹ | **1282.81** | `Fig. 7c` · 이론 1675 의 76.6 % (우리 산수) |
| 100 사이클 후 | n/a (그림에 ≈6 사이클만) | 493.20 mAh g⁻¹ | 유지율 **38.4 %** (우리 산수) · CE > 97 % |
| Li\|PUPL\|LFP | | 144.80 mAh g⁻¹, 50 사이클 96 % | `Fig. 7f,g` (그림은 100 사이클까지 그림) |

### 3c. 기계·열 (`Fig. 4b,c`)
- 인장강도 PUPL **5.11 MPa** vs PL 0.40 · PU 막 단독 2.37 MPa (`Fig. 4c` 라벨). figure-read ≈ 파단 신율 PUPL ≈40 % · PL ≈65 % · PU ≈16 %. ⚠ x 축 라벨이 "Stress (%)" — 변형률(strain)의 오기.
- TGA (N₂, 10 °C min⁻¹): `Fig. 4b` 라벨 PL 100.00 % · PUPL **92.70 %** 손실 → PUPL 잔량 ≈7.3 %.

### 3d. 전자구조 — 클러스터 DFT (`Fig. 2g`, `Table S2`)
| 양 | UiO-66/TFSI⁻ | UiO-66/S₆²⁻ | 비고 |
|---|---|---|---|
| E_bind | **−11.96 eV** | **−26.45 eV** | `Table S2` 로 재계산 −11.958 / −26.450 eV (우리 산수 · 1 Ha = 27.2114 eV) ✓ |
| Bader 전하 이동 | 0.35 e | 1.16 e | 방향·기준 원자 집합 미기재 |
| 계 전하 | 클러스터 +4 → 복합체 +3 | 클러스터 +4 → 복합체 +2 | SI `Table S2` |

band gap 은 보고하지 않는다 (클러스터 DOS 의 E_F 기준 그림뿐).

## 4. DFT/계산 방법 ★ (SI 1.7 전부)

- **code / version**: **CP2K 2025.2**, QUICKSTEP (GPW).
- **functional + vdW**: PBE + **DFT-D3(BJ)**.
- **기저 / pseudo**: 기하 최적화 **DZVP-MOLOPT-SR-GTH** · GTH 의사퍼텐셜 · 최종 에너지는 같은 구조에서 **TZV2P-MOLOPT 단일점**. (두 기저 사이 BSSE 보정 언급 **없음**.)
- **cutoff**: CUTOFF **400 Ry** · REL_CUTOFF **55 Ry**.
- **k-points**: 주기 UiO-66 최적화만 2×2×2 MP · 클러스터는 k 없음(비주기).
- **모형**: 주기 UiO-66 를 먼저 최적화 → **고립 Zr₆ 노드 클러스터 Zr₆O₄₀C₆₄H₄₄** 절단 (**링커 8개 = COO⁻ 8 + COOH 8**, "배위 불포화 Zr 자리" 포함) · **순전하 +4** (Zr⁴⁺×6 = +24 · μ₃-O²⁻ 4 = −8 · μ₃-OH⁻ 4 = −4 · COO⁻ 8 = −8 · COOH 8 = 0). 흡착 복합체 +3 (TFSI⁻) / +2 (S₆²⁻). 비주기 경계. **주변 원자 일부 고정** (어느 원자인지 미기재).
  - ⚠ 정상 UiO-66 노드는 링커 12개 배위다 — 8개면 **링커 4개 결손 노드** 를 일부러 만든 것 (우리 판독: 원자 수 C₆₄ = BDC 8 개 × 8 C).
- **결합에너지**: E_bind = E_complex − E_UiO-66 − E_adsorbate (SI 식 5) · 흡착종 TFSI⁻ (−1) · S₆²⁻ (−2) 고립 이온 기준. **용매·고분자·Li⁺ 짝이온 없음.**
- **DFT+U · AIMD · MLIP · NEB**: 없음.
- **무질서 처리**: 해당 없음 — **흡착 자세 1개씩** (자세·자리 탐색 규칙 미기재).
- **후처리**: CDD (전하밀도 차) · **Bader** (grid 기반, CP2K 가전자 밀도) · **ELF** (Becke–Edgecombe) · DOS/PDOS (**Multiwfn**).
- **결합 자리 배위 (D-2026-10-05 규칙)**: 결합 규모 ≫ 2 eV 이고 **구조 비공개** ("Data will be made available on request") → **배위 미확인**. 모형 자체가 "배위 불포화 Zr" 을 의도적으로 만든 링커 결손 노드라, 값은 *그 결손 자리의 포화 에너지 + 전하 클러스터–음이온 쿨롱 에너지* 로만 읽는다.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | (안 봄) 제조 모식도 · UiO-66 XRD (CCDC 837158 일치) · N₂ 흡착 (Type I, 961.60 m² g⁻¹) · TEM (≈150 nm) · PU SEM (섬유 ≈0.40 µm) · EDS (C/Zr/O/N) · PUPL 단면 SEM | 없음 |
| 2a–d | Zr₆ 클러스터 위 TFSI⁻ · S₆²⁻ 최적화 구조 (위·옆). 본 그림: `Fig. 2c` 에서 TFSI⁻ 는 술포닐 O 로 노드 꼭대기 Zr 에 붙고, `Fig. 2d` 에서 S₆²⁻ 는 사슬 끝 S 쪽이 노드 Zr 근처에 놓인다 — **Zr–S 원자 수·거리는 그림으로 셀 수 없다** (라벨 없음) | 흡착 자세 1개씩 · 자리 탐색 없음 — 방법 반례 |
| 2e,f | CDD 등치면 (노랑/청록, **등치면 값 미기재**). S₆²⁻ 쪽 청록 덩어리가 S 사슬 전체를 덮어 크고, TFSI⁻ 는 작다 | 등치면 값 없는 CDD 는 크기 비교 근거가 못 된다 |
| 2g | 막대: E_bind −11.96 / −26.45 eV (왼축 0 ~ −40) · Bader 0.35 / 1.16 e (오른축 0–1.8) | §10-② |
| 2h,i | ELF 2D 단면 — **색막대 숫자 없음**. figure-read: 단면이 링커 4개(십자형)가 놓인 면이고, **TFSI⁻ 와 S₆²⁻ 가 단면에 보이지 않는다**; 두 그림이 사실상 같다 | ⚠ 본문 *"Zr–S 계면 ELF 증가"* 를 이 그림이 **보여 주지 않는다** (§10-③) |
| 2j,k | Total DOS · UiO-66 PDOS · 흡착종 PDOS (−15 … +10 eV, E_F 기준). figure-read: (j) TFSI⁻ PDOS 는 ≈ −10 … −3 eV 에 넓게, E_F 근처 거의 0; (k) S₆²⁻ PDOS 는 ≈ −2 … 0 eV 에 작은 봉우리들 | 클러스터 '페르미 준위' = HOMO 기준이다 (갭 계 · 정의 미기재) |
| 2l,m | Zr 4d vs O 2p(TFSI⁻) / S 3p(S₆²⁻). figure-read: (m) 점유 영역 **−2 … 0 eV 의 S 3p 봉우리 위치에 Zr 4d 는 ≈0** — Zr 4d 는 ≈ +1.3 eV 이상 비점유대에 있고, S 3p 와 겹치는 곳은 **비점유 ≈ +2 … +3.5 eV** 뿐. (l) Zr 4d 는 ≈ +0.8 eV 이상, O 2p 는 −10 … −3 eV | 본문 *"Zr 4d–S 3p 뚜렷한 혼성"* 은 점유 상태에서 그림으로 확인되지 않는다 (§10-③) · y 축 척도가 (l) 1.2 / (m) 1.0 으로 다르다 |
| 3a | UV-vis: Li₂S₆ 용액 흡수(≈320 nm 봉우리) — PEO 담근 뒤 줄고, UiO-66 담근 뒤 가장 낮다 · 사진: UiO-66 병이 거의 무색 | 정성 흡착 증거 (UiO-66 질량·표면적 정규화 없음) |
| 3b,c | Zr 3d: 183.18/185.50 → **183.10/185.30 eV**. figure-read: (c) 에 **≈181.5 eV 저결합 성분이 새로 맞춰져 있다** (본문 언급 없음) | 이동 0.08 eV 는 XPS 대전 보정 오차 범위 · **스핀–궤도 간격이 2.32 → 2.20 eV 로 바뀐다** (우리 산수 · Zr 3d 는 고정값 ≈2.4 eV 여야 함) → 피팅 신뢰도 낮음 |
| 3d | UiO-66/Li₂S₆ S 2p: "S_B⁰" ≈170.3 eV · "S_T⁻¹" ≈169.1 eV (figure-read) | ⚠ **폴리설파이드 S 2p 는 162–164 eV 대역**이다 (저자 자신의 `Fig. S16` 본문 서술도 163.5/162.0). 169–171 eV 는 설페이트/TFSI 대역 → 지정 불일치 (§10-③) |
| 3e | C 1s: O–C=O ≈293, C–O ≈288.8, C–C ≈284.8 eV (figure-read) | 본문은 `Fig. S5` 와 비교해 카르복실 변화 주장 (S5 안 봄) |
| 3f | VB-XPS "PUPL-Sₙ²⁻" vs "PUPL-TFSI⁻" (캡션은 S₆²⁻). figure-read: Sₙ²⁻ 곡선이 **모든 결합에너지에서 위에 있고** 개시점(≈3 eV)은 같다 | 정규화 없는 a.u. 세기 차이는 *상태밀도 증가* 의 근거가 아니다 (전체 배율 차와 구분 불가) · 시료 제조법 미기재 |
| 3g | 기전 모식도 (TFSI⁻ 약한 Zr–O → Sₙ²⁻ 강한 Zr–S, "weak → strong polarization") | 개념도 |
| 4a | XRD: PU 7.30° (UiO-66) · PL 19.60°/23.10° (PEO) — PPL·PUPL 순으로 약해짐 | 정성 |
| 4b | TGA (본 §3c) | ⚠ 잔량 귀속 (§10-⑥) |
| 4c | 응력–변형 (본 §3c) | 우리 E 와 다른 양 · 다른 재료군 — 비교 안 함 |
| 4d,e | FTIR: O=S=O 1346→1348, S–N–S 651→653 cm⁻¹ · C–F ≈1197 불변 | 2 cm⁻¹ 이동 — 분해능 미기재 |
| 4f–h | Raman 735/743 cm⁻¹ 대역 디콘볼루션: free TFSI⁻ **49.40 → 78.10 %**. figure-read: (h) 의 free 성분 FWHM ≈16 cm⁻¹ 대 pair ≈6 cm⁻¹ — 두 시료에서 **폭이 자유롭게 달라진 피팅** | 폭 고정 없이 면적비를 비교했다 (§10-①) |
| 5a,b | Nyquist (25–80 °C). figure-read: PL 25 °C 반원 끝 ≈4000 Ω, PUPL 25 °C 절편 ≈150–180 Ω | |
| 5c | 구간 아레니우스 (본 §3a) — 0.35 / 0.64 (PUPL) · 0.62 / 1.15 eV (PL) | 재적합 재현 ✓ |
| 5d | LSV 접선 외삽 3.90 / 5.15 V. figure-read: PL 은 ≈5.0 V 에서 ≈0.95 mA 봉우리, PUPL 은 6 V 에서 ≈0.18 mA | 전류 문턱 미정의 · 우리 grand-potential 창과 **다른 양** |
| 5e,f | DC 분극 + 전후 Nyquist. figure-read: PL I₀ ≈44.5 → I_s ≈21 µA · PUPL I₀ ≈31 → I_s ≈20.7 µA | ΔV 미기재라 t⁺ 재계산 불가 |
| 5g | Li\|Li 0.1 mA cm⁻² 60 °C: PL ≈330 h 에서 끊김 · PUPL 1600 h. figure-read 과전압 PL ≈ ±0.06 V · PUPL ≈ ±0.035 V | |
| 5h,i | 율속 대칭셀 0.05–0.30 mA cm⁻² | |
| 6a,b | CV 등고선 (0.1–0.5 mV s⁻¹) — 봉우리 A (S₈→Li₂Sₓ), B (Li₂Sₓ→Li₂S), C (Li₂S→S₈) | |
| 6c | CV 0.1 mV s⁻¹: ΔE 0.38 (PUPL) / 0.42 V (PL). figure-read: 봉우리 C PUPL ≈0.8 mA @≈2.43 V · PL ≈0.28 mA | 같은 S 부하에서 봉우리 전류 3 배 — 양극 액체 젖음 조건 |
| 6d,e | "Tafel" (본 §3b). figure-read: `Fig. 6d` "Peak B" 는 **2.18–2.35 V · 양의 기울기**, `Fig. 6e` "Peak C" 는 **1.87–2.07 V · 음의 기울기** — 그런데 `Fig. 6c` 에서 B 는 환원(≈1.8–1.95 V), C 는 산화(≈2.4 V) | 전위 범위·기울기 부호가 **봉우리 라벨과 뒤바뀌어 보인다** · 기울기 값 자체도 비물리 (§10-③) |
| 6f,g | in-situ Nyquist (OCV → 1.7 V, 겹쳐 쌓음). figure-read: OCV 반원 PL ≈250 Ω · PUPL ≈150 Ω | |
| 6h,i | DRT 등고선 (τ 10⁻⁵–10² s · 색 0–700). figure-read: **가장 센 응답은 τ ≈10–100 s** (PL 은 거의 모든 전압에서 빨강, PUPL 은 OCV·1.8·1.7 V 에서만 약하게) | 저자의 τ 구간 정의는 τ₄ = 10⁻¹–10⁰ s 까지 — **가장 센 봉우리가 정의 밖** (§10-③) |
| 7a | GITT + log D (오른축 −10 … −40, 단위 "cm²g⁻¹" 오기). figure-read: 두 계 모두 log D ≈ −10 … −15.5 범위에 흩어짐 | 5 자릿수에 걸친 값의 "평균" 은 큰 값이 좌우한다 · 양극 겉보기 D — 전해질 물성 아님 |
| 7b,d | 충방전 곡선 (PUPL 1/2/10/50/100 · PL 1/2) | |
| 7c | 사이클: PUPL 1282.81 → 493.20 (100 cyc) · **PL 점은 ≈6 사이클까지만** (figure-read 867 → ≈640) | 본문 *"PL 보다 유지율이 훨씬 높다"* 는 PL 100 사이클 자료가 그림에 없다 |
| 7e | 첫 사이클 Q_H / Q_L 구간 | `Fig. S17` 안 봄 |
| 7f,g | Li\|PUPL\|LFP — 본문 "50 사이클 96 %", **그림은 100 사이클까지** (figure-read ≈145 → ≈130 mAh g⁻¹, ≈90 %) | 본문과 그림 사이클 수 불일치 |
| 7h | 파우치 LED (평평·굽힘·절단) | 시연 |
| S16 | ex-situ S 2p (전해질의 양극 쪽 면) @2.2/2.0/1.9/1.7 V. figure-read: "Sulfate-related S" ≈169–170 eV · **"Briding S" 라벨 봉우리 ≈167–168 eV** · "Terminal S" 화살표는 ≈162.3 eV 성분 · 라벨 없는 녹색 ≈163.8 eV 성분 | ⚠ 본문은 bridging = **163.5 eV** 라 한다 — 그림의 "Briding S" 는 4 eV 이상 높은 곳 (§10-③) · 단일 성분 피팅(2p₃/₂·₁/₂ 짝 없음) · Zr 3d 신호는 안 잡혔다고 SI 가 자인 |
| Table S1 | 온도별 σ (5 시료 × 7 온도) | §3a 재적합의 원자료 |
| Table S2 | 단일점 총에너지·순전하 | §3d 재계산 원자료 |

## 6. Post-processing ★

- **무엇**: E_bind (단일점 차) · CDD · Bader (grid) · ELF · DOS/PDOS — 전부 **흡착 자세 1개짜리 클러스터 두 개** 위에서.
- **도구**: CP2K → Multiwfn (DOS/PDOS · ELF 추정) · Bader (Henkelman 알고리즘) · 그림은 VESTA 류 볼-스틱 (명시 없음).
- **수치화·기록**: `Table S2` 에 원 총에너지 (Ha, 소수 12자리) + 순전하를 공개 — **재현 가능한 유일한 수치**. CDD 등치면 값 · ELF 색막대 값 · DOS 번짐(broadening) 폭 · Bader 원자 집합은 **모두 미기재**.
- **실험 후처리**: 구간 아레니우스 (σ = A·exp(−Ea/k_BT), σT 형 아님) · Bruce–Vincent t⁺ · GITT (ECbox, SI 식 4) · DRT (방법·정칙화 미기재) · Tafel (CV 봉우리 부근 log i–E).

### 기법 미니 용어집
- **루이스산 자리 (Lewis acid site)**: 전자쌍을 받을 수 있는 빈 궤도를 가진 자리 — 여기선 링커가 빠져 배위가 비는 Zr⁴⁺.
- **UiO-66**: Zr₆O₄(OH)₄ 노드 + 테레프탈산(BDC) 링커 12 개로 된 MOF. 링커 결손이 생기면 Zr 자리가 열린다.
- **CDD (charge density difference)**: ρ(복합체) − ρ(기판) − ρ(흡착종). 등치면 값이 같아야 두 그림 크기를 비교할 수 있다.
- **ELF**: 0–1 사이 전자 국소화 지표. 2D 단면은 **그 면에 놓인 원자만** 보여 준다.
- **VB-XPS**: 가전자대 광전자 스펙트럼 — 점유 상태 분포. 시료 간 비교엔 세기 정규화가 필수.
- **DRT (distribution of relaxation times)**: 임피던스를 이완시간 τ 분포로 바꾼 것 — 봉우리 지정은 τ 구간 가정에 달려 있다.
- **Tafel 기울기**: b = 2.303RT/(αnF). 60 °C 에서 2.303RT/F = **66.1 mV** (우리 산수) → 단일 전자 α=0.5 면 ≈132 mV dec⁻¹.
- **GITT 겉보기 D**: 양극 활물질 기준 확산계수 — 전해질 성질이 아니라 셀 전체 반응의 겉보기 값.

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 재료 | PEO-LiTFSI + PAN + UiO-66 (고분자 복합) | argyrodite Li₆PS₅Cl 계 (comp1 · modelc) | **다른 재료군 — 물성 칸 비교 없음** |
| 코드 · 범함수 | CP2K 2025.2 · PBE-D3(BJ) · GTH + DZVP/TZV2P-MOLOPT · 400/55 Ry | QE · PBE · 평면파 (우리 기준선) | 같은 PBE 계열이나 기저 체계가 다르다. CP2K 선례 셋 (`[Zhang26PI3]` 520 Ry · `[Wang26uMLP]` 900 Ry · 이 논문 400 Ry) 과 함께 **CUTOFF 가 편마다 다름** — 문헌 설정을 이식하지 않는다 |
| 모형 | 고립 **전하 +4** 클러스터 · 비주기 · 링커 4개 결손 | 주기 결정 셀 · 중성 | 전하 클러스터 결합에너지는 우리 흡착/결합에너지와 같은 줄에 놓을 수 없다 |
| 흡착에너지 규모 | −11.96 / −26.45 eV | (우리 흡착 결과 기록은 배위수를 싣는 규칙 — D-2026-10-05) | 화학결합 규모 ≫2 eV · 구조 비공개 → **배위 미확인** · 쿨롱 항 지배 |
| 이온 수송 | 실측 σ · 구간 Ea (고분자 분절 운동) | UMA-MD (절대값 비인용 · 계 간 상대차만) | 기전이 다르다 (고분자 VTF/결정화 vs 결정 홉) — **같은 표에 숫자로 두지 않는다** |
| 산화 안정 | LSV 접선 외삽 5.15 V (60 °C · 고분자) | grand-potential 산화 개시는 S-제한 2 V 대 (축 ① · 열역학) | **다른 양** (동역학 전류 개시 vs 열역학 분해 개시) · 다른 재료 |
| 전자구조 | 클러스터 DOS (E_F = HOMO 추정) · gap 미보고 | fixed-occ nscf VBM/CBM gap | 비교 대상 없음 |

**판정**: 실제 차이 vs 방법 인공물을 가를 만한 **같은 양이 하나도 없다.** 방법 반례로만 쓴다.

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **전하가 다른 두 흡착종의 결합에너지를 서로 비교하지 않는다** — 특히 전하를 띤 절단 클러스터 위에서. 이 논문의 −11.96 vs −26.45 eV 는 전하 −1 대 −2 × 클러스터 +4 의 쿨롱 차이가 대부분이고, 저자도 SI 에서 인정한다. 우리 쪽에서 Li₂Sₙ / 폴리설파이드 · 음이온 흡착을 비교할 일이 생기면 **중성 짝 (Li₂S₆ vs LiTFSI) 또는 같은 전하끼리** 로 보고량을 정의한다 (보고량 카드 §1–3).
- ② **2D ELF 단면은 단면 위치를 먼저 확인** — 흡착 계면이 단면 밖이면 그 그림은 계면 주장에 쓸 수 없다. 우리 ELF 그림(Nd · LPSCl)도 단면 면 지정과 색막대 숫자를 같이 싣는다.
- ③ **PDOS '혼성' 주장은 점유 · 비점유를 나눠 말한다** — 이 논문은 비점유 영역의 겹침을 '강한 혼성' 으로 서술했다. 우리 COHP/ICOHP 를 이미 쓰고 있으므로 결합 세기는 그쪽 숫자로 말한다.
- ④ **대조군 행은 표 안에 있는데 결론에 안 쓰인 경우를 찾는다** — PPL 행이 그렇다. 우리 원고도 대조 계산(예: O 단독 대조)이 결론과 어떤 비율로 연결되는지 한 줄을 싣는다.
- ⑤ Li–S 양극 쪽 S 2p 지정 참고점: 폴리설파이드 bridging ≈163.5 · terminal ≈162.0 eV (이 논문 본문 서술) — 단 이 논문의 그림 라벨과 어긋나므로 **이 편을 XPS 기준점 출처로 쓰지 않는다** (우리 `xps_reference_sei.csv` 기준점은 따로 있다).

## 9. 인용 가능 문장 (deck/paper용)

- "A PAN/UiO-66 nanofiber-reinforced PEO/LiTFSI electrolyte showed 3.75 × 10⁻⁴ S cm⁻¹ at 60 °C, compared with 1.30 × 10⁻⁴ S cm⁻¹ for PEO/LiTFSI and 3.54 × 10⁻⁴ S cm⁻¹ for the UiO-66-free PAN/PEO/LiTFSI control (Shang *et al.*, *Chem. Eng. J.* 2026, Table S1)." — 대조군까지 같이 인용할 때만.
- "Binding energies computed on a positively charged truncated Zr₆ cluster (+4) for anions of different charge (TFSI⁻, S₆²⁻) are dominated by long-range electrostatics, as the authors note." — 방법 반례로.
- ⛔ 인용 금지: *"UiO-66 Zr⁴⁺ sites raise ionic conductivity 2.8-fold"* (대조군 PPL 이 1.06 배로 반박) · *"S₆²⁻ binds more strongly than TFSI⁻ (−26.45 vs −11.96 eV)"* (전하 교락) · *"solid-state Li–S"* 를 액체 없는 셀로 서술 · 이 논문의 t⁺ · GITT D · σ 를 우리 계산값 옆에 같은 양으로 두는 것.

## 10. 주의/한계 (over-claim 방지)

- **① 귀속 대조 부재 — 가장 큰 결함.** σ 향상의 귀속(Zr⁴⁺–TFSI⁻) 근거는 FTIR 2 cm⁻¹ 이동과 Raman 면적비인데, Raman 피팅은 성분 폭이 시료마다 자유롭다 (figure-read FWHM ≈16 vs ≈6 cm⁻¹). 그리고 같은 SI `Table S1` 의 **PPL (UiO-66 없음)** 이 60–80 °C 에서 PUPL 과 1.01–1.06 배다 (우리 산수). **PPL 의 Raman · t⁺ · Li–S 셀은 보고되지 않았다** — UiO-66 이 셀 성능에 무엇을 더했는지 가를 실험이 없다. UiO-66 은 PUPL 질량의 **0.67 wt%** 다.
- **② DFT 모형이 결론을 받치지 못함.** (a) 클러스터 +4 · 흡착종 −1/−2 → E_bind 차이 대부분 쿨롱 (저자 인정 · "might be somewhat overestimated"); (b) 흡착 자세 1개씩 · 자리 탐색 없음 · 구조 비공개 → 배위 미확인; (c) 용매 · 고분자 · Li⁺ 짝이온 없음 — 실제 경쟁은 *LiTFSI 해리 상태 대 Li₂Sₙ* 이지 맨 음이온끼리가 아니다; (d) 두 기저(DZVP 최적화 → TZV2P 단일점) 사이 BSSE 보정 없음; (e) **'경쟁 치환' 반응에너지 (복합체/TFSI⁻ + S₆²⁻ → 복합체/S₆²⁻ + TFSI⁻) 를 계산하지 않았다** — 계산 두 개로 바로 낼 수 있는 양인데, 그것도 전하가 바뀌는 반응이라 같은 교락이 남는다.
- **③ 그림–본문 불일치 (본 그림 기준).** `Fig. 2h,i` ELF 단면에 흡착종이 없다 · `Fig. 2m` 점유 S 3p 위치에 Zr 4d ≈0 · `Fig. 3c` Zr 3d 스핀–궤도 간격 2.32 → 2.20 eV (물리 상수여야 함) + 언급 없는 ≈181.5 eV 성분 · `Fig. 3d` 폴리설파이드를 169–171 eV 에 지정 · `Fig. S16` "Briding S" ≈167–168 eV vs 본문 163.5 eV · `Fig. 6d,e` 봉우리 라벨과 전위 범위·기울기 부호가 뒤바뀌어 보임 · Tafel 15.45 / 16.75 mV dec⁻¹ → αn ≈ **4.3 / 4.0** (60 °C, 우리 산수 — 단일 전자 이동으로는 비물리; CV 봉우리 부근은 확산 제한이 섞여 Tafel 영역이 아니다) · `Fig. 6h,i` DRT 최강 봉우리 τ ≈10–100 s 가 정의 구간(≤10⁰ s) 밖 · `Fig. 7c` PL 은 ≈6 사이클뿐인데 "유지율 비교" · `Fig. 7f` 는 100 사이클인데 본문은 50 사이클 96 %.
- **④ "고체" 가 아니다.** S 양극에 액체 전해액 5 µL (DOL/DME + LiNO₃). 폴리설파이드 용해·셔틀이 액체 상에서 일어날 수 있고, LiNO₃ 는 Li 음극 보호 첨가제다. 황 변환 지표 (CV · Tafel · DRT · 용량) 는 이 혼성 조건의 값이다. 또 모든 시험이 **60 °C** (PEO 융점 부근) — 상온 성능은 σ 25 °C 3.92×10⁻⁵ S cm⁻¹ 뿐.
- **⑤ 겉보기 Ea 는 홉 장벽이 아니다 (홉 수 검산, D-2026-09-27).** Γ = ν₀·exp(−Ea/kT), ν₀ 10¹³ s⁻¹ 가정: PL 저온 **1.15 eV @298 K → Γ ≈ 3.6×10⁻⁷ s⁻¹ · 1/Γ ≈ 2.8×10⁶ s (≈32 일)** — 그런데 측정 σ 는 1.48×10⁻⁶ S cm⁻¹ 로 잰다 ⇒ 1.15 eV 는 단일 홉 장벽이 아니라 **결정 PEO → 비정질 전이가 섞인 겉보기 기울기**다. PUPL 고온 0.35 eV @333 K → Γ ≈ 5.1×10⁷ s⁻¹ · 1/Γ ≈ 20 ns (차수 검산이지 D·σ 아님). 구간 분할 (60 °C 를 어디에 넣느냐) 에 따라 값이 바뀐다.
- **⑥ TGA 잔량 귀속 질량수지 불일치 (우리 산수).** 본문: PUPL 800 °C 잔량은 "주로 UiO-66 → ZrO₂". 그런데 UiO-66 은 0.67 wt% 이고 Zr₆O₄(OH)₄(BDC)₆ (≈1664 g mol⁻¹) → 6 ZrO₂ (≈739 g mol⁻¹) 면 ZrO₂ ≈ **0.30 wt%** 다. `Fig. 4b` 라벨상 잔량 ≈7.3 % 의 대부분은 N₂ 중 **PAN 탄화 잔류물** (PAN 8.28 wt%) 로 보는 것이 자연스럽다.
- **⑦ 숫자 정밀도 과장.** 1282.81 mAh g⁻¹ · 961.60 m² g⁻¹ · 0.40 µm 처럼 반복 재현 오차 없이 유효숫자를 많이 쓴다 — 셀 수 · 오차막대 전부 미기재 (단일 셀로 보인다).
- **⑧ t⁺ 재현 불가.** Bruce–Vincent 에 필요한 ΔV 미기재. 고분자 전해질 t⁺ 0.21 → 0.65 는 큰 변화인데 PPL 대조가 없다.
- **⑨ 지위.** Journal Pre-proof — 최종판에서 그림·수치가 바뀔 수 있다.

## 11. 우리 쪽 원장 대조 (인용 전 30초)

- 우리 값을 이 digest 에 숫자로 옮기지 않았다. §7 의 "S-제한 2 V 대" 는 정성 표현이고, 창 폭 (`window_V`) 은 `HZ-esw-reduction-limit-label` 로 걸려 있어 인용하지 않았다 (`db/properties/citation_hazards.json`).
- 우리 σ · D · Ea 는 1저자 인용정책(2026-09-18)상 계 간 상대차로만 쓴다 — 이 논문 값과 한 줄에 두지 않는다.
- comparison_vs_ours.md 등록 제안 (부모 세션 몫): A–D 물성 표 **아님** · `🔧 방법 원전/반례` 블록 한 줄 — *"전하 클러스터 위 서로 다른 전하 음이온 결합에너지 비교 (−11.96 vs −26.45 eV) = 쿨롱 교락 · 배위 미확인"* · `[Yuan26LCE]` · `[Yu26Pol]` · `[Meng26LZF]` 반례 계열에 추가.

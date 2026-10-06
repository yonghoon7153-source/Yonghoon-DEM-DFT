<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = zuo2022_chlorination_cathode_interface.md.
     ★ = 1저자가 특히 요청한 항목 (LPSCl@Li₂S 볼밀 복합체의 "중간 비정질상" 가설 — 원출처 검증).
     같은 논문의 첫 digest(DEM/FEM 축) = cronk2026_lis_positive_electrode_geometry_fem.md — 기하·τ·응력·고로딩은 그쪽. -->
# 1-step 고에너지 밀링 Li–S 양극의 **계면상 화학** — S 표면 Li₃PS₄₊ₙ 과 **Li₂S 양극에서의 LPSCl→"LPS-like" 분해** — Cronk et al. (Nat. Commun. 2026) [두 번째 읽기축]

> slug `cronk2026_lis_cathode_interphase_chemistry` · DOI `10.1038/s41467-026-69750-0` · type `exp (XRD · Raman · S K-edge XANES/LCF · TGA · cryo-(S)TEM-EDS · EIS · dQ/dV · CV; 원자계산 0)` · PDF `litdb/inbox/104. Bai2026_A_highly_utilized_and_practical_LiS_cathode_enabled_in_ASSBs.pdf` (본문 15 pp) + `104. Sup) …pdf` (SI 45 pp, Fig S1–S35 · Table S1–S8) + `104. Sup1) Bai2026_source_data.xlsx` (Source Data 30 시트) · digested `2026-09-11` · status ✅
> elements: Li, P, S, Cl, C, Si
> methods: Raman
> 🔗 **관련 (2026-10-06)**: `lee2025_halide_segregation_uhs_mixing_li_chalcogen_assb` — Science 2025 · S/Se 계 2000 rpm 원심혼합에서 LPSCl 의 Cl 이 칼코겐 표면 LiX 로 편석한다는 주장(이 논문이 보고 안 한 Cl 행방의 S 계 답) · 본문 미확보, SM 기준.
> **저자**: **Ashley Cronk**¹, Xiaowei Wang², Jin An Sam Oh², So-Yeon Ham¹, **Shuang Bai**¹, Phillip Ridley², Mehdi Chouchane³, Chen-Jui Huang³, Diyi Cheng², Grayson Deysher¹, Hedi Yang³, Baharak Sayahpour¹, Marta Vicencio², Choonghyeon Lee⁴, Dongchan Lee⁴, Min-Sang Song⁴, Jihyun Jang², **Jeong Beom Lee**⁴\*, **Ying Shirley Meng**²,³\* — ¹UCSD MSE · ²UCSD NanoEngineering · ³UChicago Pritzker (PME) · ⁴**LG Energy Solution** (LG Science Park, Seoul). *Nature Communications* **17**, 3298 (2026). 접수 2025-03-25 / 수리 2026-02-09. OA (CC-BY). 특허 2건 출원(UCSD + LGES). 자금: LGES–UCSD Frontier Research Laboratory.
>
> ⚠ **파일명·저자 정정 (2026-09-11)**: inbox #104 의 파일명 `Bai2026_…` 은 **오기**다. 1저자는 **Ashley Cronk** 이고 **Shuang Bai 는 5저자**(Author contributions: *"S.B. contributed cryo-TEM characterization and investigation"*). 이 Shuang Bai(UCSD MSE)는 litdb 의 `bai2020_argyrodite_review_progress`(**Xiangtao Bai**, 中国汽车动力电池研究院, Beijing)와 **다른 사람**이다. 또한 이 PDF 는 **inbox #64 와 같은 논문**(DOI 동일)이다.
>
> 🔗 **같은 논문의 첫 digest** = `cronk2026_lis_positive_electrode_geometry_fem.md` (2026-09-03, DEM/FEM 축: 확률적 voxel 기하·TauFactor τ·COMSOL 응력·입경·부피변화·고로딩·파우치). **이 카드는 그 카드가 30줄로 요약하고 지나간 §6.1–6.2(계면상)를 1저자의 가설 검증 목적으로 전부 다시 판다.** 두 카드가 어긋나면 계면상·공정·복합체 σ 에 관해서는 **이 카드가 이긴다** (Source Data 원시값까지 대조했다). 기하·FEM·응력·에너지밀도는 그쪽이 정본.
>
> 🎤 **관련 발표**: 없음 — `litdb/talks/*.md` 의 "논문 에이전트 인입 대기열" 에 이 논문 행 없음 (2026-09-11 grep).
>
> 📦 **Source Data 처리**: 30 시트 중 ★질문에 걸리는 **11 시트**(Fig. 2a-d · S3 · S4 · S5 · S6c/S7c · S8 · S9 · S10 · S11 · S12 · S13)를 long-format CSV 로 전사해 `litdb/inbox/104_source_data/cronk2026_source_<fig>.csv` 에 두었다 (**inbox 는 gitignore — 저장소 밖**, ~45 MB; 원본은 `litdb/inbox/104. Sup1) Bai2026_source_data.xlsx`). 저장소에 남긴 것은 그 원시값에서 뽑은 **파생 요약표** `litdb/figures/cronk2026_lis_cathode_interphase_chemistry/source_data_derived.csv` (Raman 피크·XANES 미분극대·EIS R·역산 두께·TGA·EDS 조성·용량·XRD FWHM; `_sources.json` 등록) 뿐이다. 인용한 수치는 전부 이 카드 본문 표에 직접 적었다. `db/properties/` 에는 아무것도 만들지 않았다(문헌 소환값이라 우리 원장이 아니다). 나머지 시트 목록은 §20.

---

## 0. 이 digest 를 읽는 법 — 1저자의 가설이 이 논문의 *어느 문장*에서 왔는가

우리 캠페인의 가설: **"LPSCl@Li₂S 볼밀 복합체의 계면에 중간 비정질상이 생겨 이온전도를 살린다."** 이 논문에는 그 문장을 지탱하는 서사가 **둘로 갈라져** 있고, 둘을 섞으면 안 된다.

| | **S 양극** (S₈ + LPSCl + C) | **Li₂S 양극** (Li₂S + LPSCl + C) — **= 우리 계** |
|---|---|---|
| 논문의 명명 | *"sulfur-rich ionically conductive interlayer/interphase **Li₃PS₄₊ₙ**"* (Fig. 2e, p3–4) | *"**decomposition and amorphization of LPSCl** … Li₂S **reduces** LPSCl to **LPS**"* (p4) |
| 생성 기구(저자) | S 가 PS₄³⁻ 말단 S 와 **결합**(가교 S–S) — *interfacial reaction* | LPSCl 의 **분해** (→ Li₃PS₄-like); *"Usually formed electrochemically, here the redox active products are formed during synthesis"* |
| 이온전도 서술 | S/LPSCl 복합 σ **6×10⁻⁶ → 2×10⁻⁵ S cm⁻¹** (1 h) — *"supports the formation of the ionically conductive sulfur rich phase"* (p4) | *"Despite the catholyte decomposition and **reduction in composite ionic conductivity** (Fig. S10c), the Li₂S cell exhibits stable cycling"* (p4) — 그리고 p6 에서는 *"the amorphous LPS/LPSCl mixture **retains** its ionic conductivity, supported by the Li₂S electrochemical performance"* |
| 조성 특정 | n 은 용량(553 mAh g_S⁻¹)에서 역추정 → *"likely Li₃PS₄₊₃"* (p5) | **특정 안 함** — "LPS", "amorphous LPS/LPSCl mixture" 까지. LiCl·Li₇PS₆·Cl 행방 언급 **0** |
| 직접 증거 | XRD 비정질화 · TGA 6.5 wt% 미회수 S · Raman 149/420 cm⁻¹ · XANES "pre-edge" · STEM-EDS S:P 과잉 · dQ/dV 1.3 V 영역 · σ 상승 | XRD 아지로다이트 피크 소멸 · Raman PS₄³⁻ 425→418 · XANES LCF LPSCl 절반→LPS · Nyquist(σ 미보고) · 셀 성능 |

⇒ **1저자 가설의 "이온전도를 살린다" 부분은 S 양극 서사에서 왔고, Li₂S 양극(우리 계)에 대해 논문이 직접 보여준 것은 "LPSCl 이 비정질 LPS-like 로 분해돼도 셀이 잘 돈다(723 mAh g⁻¹, CE 99.3 %)" 까지다.** 이 구분이 이 카드 전체의 뼈대다 (§5·§7·§8·§14).

## 1. 한 줄 요약

500 rpm · 1 h · 시료:볼 1:30 의 **1-step 고에너지 유성밀**로 S(또는 Li₂S) : LPSCl : AB = 30 : 50 : 20 wt% 를 한꺼번에 갈면, (i) S 양극에서는 S 입자 표면에 **S-풍부 티오포스페이트 Li₃PS₄₊ₙ** 계면상이 생겨(XRD 비정질화·TGA 미회수 S 6.5 wt%·Raman·XANES·STEM-EDS) S 이용률이 이론치 근처(1451–1615 mAh g_S⁻¹, CE 129–134 % = LPSCl 자체 용량 기여)로 오르고, (ii) **Li₂S 양극에서는 같은 공정이 LPSCl 을 "LPS(Li₃PS₄)-like" 로 분해·비정질화**시키지만(아지로다이트 XRD 피크 소멸, PS₄³⁻ 425→418 cm⁻¹, XANES LCF LPSCl 33.2 / LPS 31.2 / Li₂S 35.6 wt%) **셀은 723 mAh g⁻¹·CE 99.3 %** 로 잘 돌고 2사이클부터 SSE-redox 숄더가 추가된다. 계면상의 **조성·Ea·전자전도는 재지 않았고 Li₂S 복합체의 σ 는 숫자로 보고되지 않았다**(Nyquist 만). **원자 계산 0.**

## 2. 메타 — 이 논문이 litdb 에서 차지하는 자리

| 항목 | 내용 |
|---|---|
| 연구유형 | 실험(합성·전기화학·분광·현미경) + 연속체 모델링(확률적 기하·τ·FEM; 옆 카드) — **DFT/AIMD/MLIP 없음** |
| 소재계 | **Li₆PS₅Cl (NEI)** 촉매전해질/분리막 · β-Li₃PS₄ (NEI, 대조) · S (99.98 %, Sigma) · Li₂S (99.98 %, Sigma) · AB / VGCF / KB 탄소 · 음극 Li₀.₅In / Li₁In / Li₂Si / μSi / anode-free(Ag-C) |
| 핵심 질문(논문) | 황화물 SE 로 Li–S 전환형 양극의 **이용률·수명·고로딩**을 어떻게 동시에 잡나 — 답: 1-step 밀링 계면상 + SSE redox 활용 + 마이크론 입경 + 부피변화 상쇄 |
| 우리 질문(이 카드) | **LPSCl 과 Li₂S 를 볼밀하면 계면에 무엇이 생기고, 그것을 어떻게 알았고, 그것이 전도하나** (★1–7) |
| 조성 일치 | 그들 Li₂S : LPSCl = **30 : 50 wt%** → 몰분율 **x_Li₂S = 0.778** — `db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json` 의 1저자 지정점(3 : 5 wt, x = 0.778)과 **정확히 같다** |
| 관련 카드 | `cronk2026_lis_positive_electrode_geometry_fem`(같은 논문) · `lai2020_li2s_interfacial_layer_amorphous_sulfide_cse`(Li₂S 계면층 0.22 eV 귀속) · `deklerk2016_diffusion_site_disorder_argyrodite`(Li₇PS₆ vs Li₆PS₅Cl 확산) · `zuo2022_chlorination_cathode_interface`(LPSCl 산화 산물) |

## 3. 핵심 수치 총정리 (전부 문헌 소환값 · 조건 병기)

| 물성 | 값 | 조건 / 출처 | 비고 |
|---|---|---|---|
| σ LPSCl 촉매전해질(400 rpm 2 h 전밀링) | **2 mS cm⁻¹** | Ti\|SSE\|Ti, 75 MPa, 25 °C, 30 mV, 7 MHz–100 mHz — Fig. S8a | 본문 p4 |
| σ β-Li₃PS₄ (LPS) | **0.04 mS cm⁻¹** | 동일 — Fig. S8a | LPSCl 의 1/50 |
| σ LPSCl 단독 밀링 500 rpm | pristine **1.8×10⁻³** → 1 h **1.3×10⁻³** → 10 h **4×10⁻⁵ S cm⁻¹** | Fig. S4f 범례; 본문 "1.3×10⁻³ → 4×10⁻⁵" | 10 h 에 **Li₂S(XRD) + LPS(Raman 422 cm⁻¹, P₂S₆⁴⁻ 어깨)** 석출 |
| σ S/LPSCl 복합(탄소 없음, 500 rpm) | 0.5 h **6.0×10⁻⁶** → 1 h **2.1×10⁻⁵** → 10 h **2.0×10⁻⁵ S cm⁻¹** | Fig. S4c 범례 (⚠ S:LPSCl 비 미기록) | 1 h 이후 **포화**(10 h 도 같음) — LPSCl 단독의 붕괴와 대조 |
| **σ Li₂S/LPSCl 복합** | **미보고** — Nyquist R_lowf **1145 Ω (1 h) → 2675 Ω (10 h)** | Fig. S10c; Source Data 시트 `Fig. S10` (digest 추출) | 두께 미기록. 같은 프로토콜 펠릿의 역산 두께 0.44–0.55 mm 일정 → 같은 두께면 ≈ **5–6×10⁻⁵ / 2.5×10⁻⁵ S cm⁻¹** (**digest 추정**, §7) |
| Ea (어느 것이든) | **n/a** | 온도의존 EIS 없음 | |
| 전자전도 σ_e | **n/a** | DC 분극 없음 | |
| S 이용률 1-step (30 wt%, 1 mg_S cm⁻²) | 방전 **1451**(Fig. 2a xlsx) / **1615**(Fig. S3a·S8b xlsx) mAh g_S⁻¹, 충전 1943 / 1923 / 2176 | C/20 = 80 mA g⁻¹, Li₁In, 75 MPa, 25 °C | 본문 "~1500, CE 129 %"; xlsx 로는 134 % / 119 % / 135 % (§17) |
| S multi-step / hand-mix | 599 (CE 17 %) / 183 mAh g_S⁻¹ | Fig. 2a | multi-step = S+C 밀링 후 SSE 손혼합 |
| S 밀링 세기 | 300 / 400 / 500 rpm → **565 / 953 / 1615** mAh g_S⁻¹ | Fig. S3a (xlsx) | 본문 "lower intensities → lower utilization" |
| S 촉매전해질 LPS vs LPSCl | 1147 vs 1615 mAh g_S⁻¹, 분극 0.58 vs 0.54 V | Fig. S8b, 1.6 mAh cm⁻² | |
| **Li₂S 1-step** (30 wt%, Li₀.₅In) | 충전 **724 / 방전 720** mAh g⁻¹ (본문 723, **CE 99.3 %**) | Fig. S9 xlsx, C/20 = 60 mA g⁻¹ | multi-step 378/252 · hand-mix ≈ 0 |
| Li₂S 사이클 진행 | 방전 720 → 728 → 739 → 744 (1→4 cyc) | Fig. S11 xlsx | 2 cyc 부터 충전 ~2.5–2.7 V 숄더 = *"SSE redox"* |
| TGA 미회수 S (1-step S 양극) | **6.5 wt%** of composite (= 30 − 23.5) | Fig. S5, N₂, 5 °C/min, 450 °C 종점 | 450 °C 에서 곡선 미평탄(−0.055 %/°C) → **상한**(§17) |
| TGA 10 mAh cm⁻² 전극 | pristine 20 % reacted · 방전 93.1 % · 충전 34 % | Table S4 / Fig. 4c (23.7 / 2.1 / 19.7 % 질량손실) | Fig. 4c 라벨은 23.4 % |
| Raman S–S 굽힘 (E₂) | S₈ **152.4** · mixed S/LPSCl **152.4** · **milled S/LPSCl 152.4** · 1-step 전극(탄소 포함) **149.1** cm⁻¹ | Source Data `Fig. 2c` 최대값 | ⚠ 본문 "milled S and LPSCl **and** one-step … redshift" — 탄소 없는 시료는 **이동 없음** |
| Raman PS₄³⁻ 신축 | LPSCl **425.8** → milled S/LPSCl **420.4** (강도 0.31→0.07) · LPSCl 10 h **422.1** · **milled Li₂S/LPSCl 420.4**(그림 라벨 418; 강도 0.74→0.095) | Source Data `Fig. S4b/S4e/S10b` | β-LPS 기준 418(Fig. S16 fit 417.3) |
| XANES S K-edge | 1-step 전극 1차미분 극대 **2471.0 eV** · LPSCl **2471.8** · S₈ **2472.0**(백색선 2473.6) | Source Data `Fig. 2d`; 그림 라벨 2471.0 / 2472.4 / 2473.6 | 본문 "pre-edge **2470.1** eV" 는 오타로 보임 |
| XANES LCF (wt%, 종 기준 합 100) | S/LPSCl/C pristine **S 38.4 / LPSCl 61.6** (χ² 0.24) · **Li₂S/LPSCl/C pristine LPSCl 33.2 / LPS 31.2 / Li₂S 35.6** (χ² 0.050) | Table S5 (SI p42 이미지 판독) | Li₂S 명목 37.5 → **Li₂S 소모 없음** |
| STEM-EDS (S 양극 응집체) | Table S1: S 68.7 / P 7.8 / Cl 6.9 / **O 16.7** at% (입자 1) · 65.8/7.6/6.7/19.9 (입자 2) | Fig. S6·S7, 200 kV cryo | 라인스캔 내부 S:P 6.8–8.1 (LPSCl 5) — §6 |
| LPSCl/C 단독 redox (1–3 V) | 환원 **115** / 산화 **355** mAh g⁻¹ (20 mA g⁻¹) · 가역 ≈ 325 | Fig. 3a, S12 xlsx | LPS/C: 171 / 312 |
| LPSCl/C (3.5–1 V, Li₂S 창) | 가역 ≈ **415** mAh g⁻¹ | Fig. S13 xlsx, 30 mA g⁻¹ | |
| dQ/dV 전위 | LPSCl 환원 **1.15 V** · Li₃PS₄₊ₙ **1.3 V** · S⁰→S²⁻ ~1.9–2.0 · Li₂S 산화 **2.37** · SSE 산화 시작 **2.70 V** | Fig. 3c,d | 모두 vs Li/Li⁺ (Li-In +0.625 V 환산, xlsx 머리) |
| 용량 기여(30 wt% S, 2.5 mg) | 방전: 미반응 S 83.3 / Li₃PS₄₊ₙ 7.5 / LPSCl 9.2 % · 충전: 62.1 / 10 / 27.5 % | Table S2 | 반응 S 비용량 **553 mAh g⁻¹** |
| 셀 조건 | 펠릿 10 mm(0.785 cm²), 분리막 375 MPa 3 min → 450–500 µm, 양극 375 MPa 5 min, LiIn 125 MPa 30 s, **스택 75 MPa**, 25 ± 1 °C; 파우치 3.24 cm², WIP 500 MPa @80 °C, **10 MPa @60 °C** | Methods p12 | |

## 4. ★3 공정 조건 — 볼밀·비율·분위기 (Methods p11–12, 원문 그대로 + 몰비 환산)

- **분위기/전처리**: Ar 글러브박스 (<1 ppm H₂O·O₂); 비무수물은 80 °C 진공건조. 시료 보관 22 ± 3 °C, 1–4 주 내 사용.
- **촉매전해질 전밀링**: *"LPSCl was milled in an argon environment at **400 rpm for 2 h** with **5 mm spherical yttria stabilized zirconia media** using a high energy planetary ball mill (**Retsch**)"* → 마이크론 LPSCl (Fig. S2). β-Li₃PS₄ 도 동일.
- **활물질 입경 조절**: S 는 as-received(~100 µm급) 또는 **400 rpm, 10 h(micron) / 24 h(sub-micron)**, 시료:볼 **1:10**. Li₂S 도 *"milled following similar procedures as sulfur"* (as-received ~30 µm → micron, Fig. S24).
- **복합체 (★)**: *"optimal positive electrode composites were milled for **1 h** … at **500 rpm** … planetary ball mill with a sample to mill media weight ratio of **1:30**"*. 조성 **30 wt% AM(S 또는 Li₂S) : 50 wt% LPSCl : 20 wt% 탄소(AB 기본; VGCF·KB 는 Fig. S29)**. ⚠ 복합체 밀링의 **볼 크기는 재기술되지 않음**(전밀링과 같은 5 mm YSZ 로 읽히지만 명시 없음), **용기 재질·볼 개수·분위기(밀링 자 내부 Ar 여부)·냉각 간격 미기록**.
- **대조 공정**: multi-step = S(또는 Li₂S)+탄소만 500 rpm 1 h 밀링 후 SSE 를 **손혼합**; hand-mix = 막자사발 1 h. (Fig. S1)
- **세기·시간 변주**: 300 / 400 / 500 rpm (Fig. S3, 탄소 포함 S 양극); **0.5 / 1 / 10 h**(Fig. S4a–c, **S + LPSCl 만**, 탄소 없음 — ⚠ 이 조성비는 미기록); LPSCl 단독 1 / 10 h (Fig. S4d–f); **Li₂S + LPSCl 1 / 10 h**(Fig. S10c; XRD·Raman 은 "milled" 만, 시간 미표기 → 기본값 1 h 로 읽힘).
- **몰비 환산 (digest 계산)** — M(Li₂S) 45.95 · M(Li₆PS₅Cl) 268.40 · M(S) 32.06:
  - Li₂S 30 : LPSCl 50 wt → n = 0.6529 : 0.1863 mol → **Li₂S : LPSCl = 3.50 : 1 → x_Li₂S = 0.778** (우리 prereg 카드와 동일).
  - S 30 : LPSCl 50 wt → S 원자 0.936 mol : LPSCl 0.186 mol → **S : LPSCl(=P) ≈ 5.0 : 1** (S₈ 로는 0.63 : 1). 전부 결합하면 Li₃PS₉ 까지 가능하지만, TGA 미회수 6.5 wt% = 0.203 mol S → **P 당 평균 1.1 S** 만 반응; 저자가 말하는 Li₃PS₄₊₃ 이면 LPSCl 의 **약 36 %** 만 변환된 셈 (digest 산술, 논문 미언급).
  - 10 / 20 wt% S 셀(Fig. 3c): LPSCl 70 / 55 wt% (Table S3).
- **전극/셀**: 펠릿(§3) · 건식 PTFE 1 wt% 핫롤 200–300 µm 필름(4.5–6 mAh cm⁻²) · 파우치(LPSCl 98 + 아크릴레이트 2 wt% 필름 50 µm; Ag-C anode-free 층 69.75 : 23.25 : 7.0).

## 5. ★1 무엇이 생긴다고 하는가 — 논문의 문장과 그 근거의 사정거리

### 5.1 S 양극: "sulfur-rich thiophosphate **Li₃PS₄₊ₙ**" 계면상
- **문장**: *"a redshift … suggests an increase in bond lengths from P–S stretching, confirming the formation of sulfur rich thiophosphates (Li₃PS₄₊ₙ), where elemental sulfur bonds with the sulfur at the PS₄³⁻ terminals of LPSCl"* (p4, refs 15 Kim 2023 · 32 Lin 2013). *"The pre-edge observed here is likely from chains of sulfur in Li₃PS₄₊ₙ"* (p4). *"The specific capacity of the reacted sulfur is estimated to be 553 mAh g⁻¹ … **likely existing in the Li₃PS₄₊₃ phase** after synthesis"* (p5).
- **위치**: *"formed on the particle surface"*, Fig. 2e 모식도 — S 입자 껍질. 두께·연속성은 **미측정**(STEM 라인스캔이 그 자리라고 주장하지만 §6.1 참조).
- **n 의 근거**: 계면상 조성을 잰 것이 아니라 **용량 산술**이다 — 2.5 mg 전극에서 미반응 S 23.5 wt% → 1 mAh(1675 mAh g⁻¹), 총 방전 1.20 mAh 중 dQ/dV 1.3–1.15 V 구간 0.09 mAh 를 반응 S(6.5 wt% = 0.1625 mg)에 배정 → 553 mAh g⁻¹ ≈ 1675/3 → "n = 3". 즉 **Li₃PS₇ 은 전기화학적 추정**이지 분광 동정이 아니다.
- **무엇이 아닌가**: 새 결정상은 XRD 에 **없다**(Fig. 2b·S4a: 피크 소멸·확폭·hump 뿐). LiCl 석출·Li₇PS₆·Li₂S 생성은 S 양극 합성 단계에서 **언급 없음**(Li₂S 는 방전 후에만, Fig. 4b).

### 5.2 Li₂S 양극 (우리 계): "LPSCl 의 분해·비정질화 → **LPS**"
- **문장 전문**(p4): *"With the Li₂S cathode, the synthesis method resulted in the **decomposition and amorphization of LPSCl**, evidenced by undetectable peaks in the diffraction pattern and a shift of P–S stretching in PS₄³⁻ from 425 cm⁻¹ to 418 cm⁻¹, assigned to Li₃PS₄ (LPS)⁴⁶ (Fig. S10a–b). This indicates that **Li₂S reduces LPSCl to LPS**. Despite the catholyte decomposition and reduction in composite ionic conductivity (Fig. S10c), the Li₂S cell exhibits stable cycling, where additional plateaus present in the voltage profile are attributed to SSE redox after the 1st cycle (Fig. S11). This confirms the redox activity from LPSCl decomposition products. **Usually formed electrochemically, here the redox active products are formed during synthesis.**"*
- **정량**(p6, Table S5): *"half of LPSCl decomposes into LPS after synthesis (Fig. 4f)"* — LCF: LPSCl 33.2 / LPS 31.2 / Li₂S 35.6 wt% → LPS/(LPSCl+LPS) = **48 %**. Li₂S 35.6 ≈ 명목 37.5(탄소 제외) → **Li₂S 는 소모되지 않았다**.
- **조성 특정 여부**: **못 했다.** 저자 어휘는 "LPS", "LPSCl decomposition products", "amorphous LPS/LPSCl mixture"(p6) 까지. **LiCl 은 합성 산물로 한 번도 거론되지 않고**(전기화학 분해식에서만 등장), **Li₇PS₆ 는 논문 전체에 0회**, Cl 의 행방(LiCl 결정? 비정질 Li–P–S–Cl? 잔류 아지로다이트?)은 **미보고**. ⁷Li/³¹P NMR · PDF · XPS · TEM(Li₂S 계) **전부 없음**.
- ⚠ **"reduces" 는 화학적으로 부정확하다.** Li₆PS₅Cl → Li₃PS₄ + Li₂S + LiCl 은 산화수 변화가 없는 **분해(불균화 없는 상분리)**다. Li₂S 가 환원제일 이유가 없고, 실제로 **LPSCl 단독 10 h 밀링도 같은 산물(Li₂S XRD + LPS Raman 422 + P₂S₆⁴⁻)**을 낸다(Fig. S4d,e). Li₂S 가 있으면 1 h 만에 아지로다이트 피크가 사라지는 것(vs 단독 10 h 에도 잔존)은 "가속" 이지 "환원" 이 아니다 — 가속의 원인(경질 Li₂S 의 연마 효과인지, 조성이 Li₂S 쪽으로 밀려 열역학적으로 LPSCl 이 더 불리해진 것인지)은 **분리되지 않았다** (§8).

## 6. ★2 증거 — 무엇으로, 어느 그림에서, 그리고 각 증거의 한계

### 6.1 S 양극 (Li₃PS₄₊ₙ)
| 증거 | 그림/표 | 관측 (본문 명시값 · Source Data 값 · figure-read ≈) | 한계 |
|---|---|---|---|
| **XRD** (Mo Kα, 모세관) | Fig. 2b · Fig. S4a | 1-step 만 비정질화: LPSCl(220) 높이 0.70→0.15, FWHM 0.25→0.36° (Fig. 2b xlsx); 탄소 없는 S/LPSCl: LPSCl(220) FWHM 0.29(mixed)→0.34°(1 h), S(222) 0.24→0.29→0.38°(10 h), 피크 높이 2–5×↓, 15–19° hump/피크 비 **0.15→0.33→0.42**(mixed→1 h→10 h) — 본문 "FWHM increases" 정량 성립 | 비정질화 ≠ 새 상. **새 피크 없음.** AB 탄소의 산란이 가려 탄소 포함 시료는 해석 불가 → 무탄소 시료로 대체(조성비 미기록) |
| **TGA** (N₂, 5 °C/min, →450 °C) | Fig. S5 · Fig. 4c · Table S4 | 23.5 % 손실(S₈ 승화) → **6.5 wt% "unaccounted"** = *"alteration of the sulfur bonding environments and possible reaction with LPSCl"*; 10 mAh cm⁻² 전극: 20 % reacted(pristine) / 34 %(charged) | Source Data: 449.5 °C 에서 76.58 %, **마지막 20 °C 기울기 −0.055 %/°C — 곡선이 평탄해지지 않았다** → 미회수분은 **상한**. "반응 S" 의 결합 형태는 TGA 가 말해 주지 않음 |
| **Raman** (785 nm) | Fig. 2c · Fig. S4b · Fig. S14 | S–S 굽힘 E₂: 1-step 전극(탄소 포함) **149.1** vs S₈ 152.4 (−3.3 cm⁻¹); 5/100 사이클 후 150.2(Fig. S14) → 부분 유지. PS₄³⁻: milled S/LPSCl **420.4, 강도 4.4×↓**(vs mixed 425.8) = *"polymerization with bridging S–S bonds"* (ref 44 Kato 2021) | ⚠ **Source Data 상 탄소 없는 milled S/LPSCl 의 S–S 굽힘은 152.4 = S₈ 과 동일** — 본문 "redshift … with the milled S and LPSCl" 은 데이터가 지지하지 않음(그림에서도 점선 위). 이동은 **탄소 포함 시료에서만** → 계면상보다 시료 상태(흡수·국소가열) 차이 가능성 배제 못 함. PS₄³⁻ −5 cm⁻¹·강도↓는 **LPSCl 단독 10 h(422)·Li₂S/LPSCl(420)** 에서도 똑같이 나타남 → **S-풍부 상 특이 신호가 아니다** |
| **XANES S K-edge** (TFY, TLS 16A1) | Fig. 2d · Fig. S17–S19 · Table S5 | 본문: "pre-edge 2470.1 eV … likely from chains of sulfur in Li₃PS₄₊ₙ" (ref 45 폴리설파이드). Source Data 1차미분 극대: 전극 **2471.0** / LPSCl 2471.8 / S₈ 2472.0; I≥0.1 도달: S₈ 2465.9 · 전극 2468.8 · LPSCl 2469.2 | (i) 2470.1 은 그림·데이터 어디에도 없음(2471.0 의 전치 오타로 보임). (ii) 전극의 edge 가 LPSCl 보다 0.8 eV 이른 것은 **S₈(2466 부터 상승)과 LPSCl 의 단순 혼합**으로도 나온다 — 별도 "pre-edge 피크" 는 미분곡선에 없다. (iii) LCF 기준 스펙트럼 집합 {S, LPSCl, LPS, Li₂S} 에 **Li₃PS₄₊ₙ 기준이 없어** LCF 는 그 상을 "볼 수 없다"; pristine S/LPSCl/C 가 χ² 0.24 로 **표에서 가장 나쁜 피팅** = 빠진 성분의 간접 흔적일 수도, 잡음일 수도. (iv) 탐침깊이 0.5–수 µm, 스팟 0.06 % 면적, 자기흡수 — SI 스스로 인정 |
| **cryo-(S)TEM-EDS** | Fig. S6 · S7 · Table S1 | ~1 µm 응집체; C/S/P/Cl 맵이 **모두 겹쳐** 분포. 라인스캔(Source Data, 길이 775 / 593 nm): 0–50 nm 거의 무신호(Cl 만 ~90 % = 카운트 0 근처), 50–100 nm **S 68–97 %**, 100 nm 안쪽부터 P·Cl·C 등장, 내부(200 nm 이후) **S/(P+S+Cl) 75–77 %, S:P 6.8–8.1, Cl:P 1.06–1.66**. Table S1(맵 정량): S:P 8.8 / 8.6 | "sulfur atomic fraction stabilizes to **double** the expected stoichiometry for LPSCl" — LPSCl 은 S:P 5, 관측 6.8–8.8 → **1.4–1.8 배**. 투과 투영이라 **S 알갱이와 LPSCl 이 겹치기만 해도** S 과잉이 나옴; 코어–셸 대비는 맵에 **보이지 않음**; **O 16.7–19.9 at%** 가 있는데 논문은 언급 없음(이송·표면산화?); Li 불가시. Li₂S 양극은 TEM 자체가 없음 |
| **dQ/dV** | Fig. 3c,d · Table S2 | 영역 II 1.3 V 환원 피크를 Li₃PS₄₊ₙ 에 배정(LPS 가 LPSCl 보다 높은 전위에서 환원, Fig. S12) → 방전 용량의 **7.5 %**, 반응 S 비용량 553 mAh g⁻¹ | 전위 순서에 의한 **간접 배정**; 10 wt% S 셀에서 가장 뚜렷 |
| **σ 상승** | Fig. S4c | S/LPSCl 0.5 h 6.0×10⁻⁶ → 1 h 2.1×10⁻⁵ → 10 h 2.0×10⁻⁵ S cm⁻¹ — *"supports the formation of the ionically conductive sulfur rich phase"* | 대안(1 h 에 S 입자 파쇄·치밀화·접촉 개선)이 배제되지 않음. 다만 **LPSCl 단독은 10 h 에 붕괴(4×10⁻⁵)하는데 S/LPSCl 은 10 h 에도 유지** — S 가 있으면 LPSCl 열화가 다른 경로를 탄다는 점은 실질적 |
| **사이클 후 보존** | Fig. 4b · S14 · S16 | 충전 후 S 가 비정질(10.5° 약피크) = *"sulfur rich interlayer is preserved"*; Raman 150.2 유지; SSE 벌크에 LPS 418 성분(fit 417.3) 출현 | 방전 시 **LPSCl 이 결정성을 되찾는다**(Fig. 4b) — 비정질화가 가역적 = 계면상이 "상" 이라기보다 "상태" 일 가능성 |

### 6.2 Li₂S 양극 (우리 계) — "LPS-like 분해"
| 증거 | 그림/표 | 관측 | 한계 |
|---|---|---|---|
| **XRD** | Fig. S10a | milled Li₂S/LPSCl (±C): **LPSCl(111)(200)(220) 소멸, (311) 높이 0.834→0.024(≈35×↓)**; Li₂S 피크는 그대로(Li₂S(111) FWHM 0.29→0.32°); 넓은 배경. mixed 는 두 상 모두 선명. 기준 β-LPS(NEI)는 그 자체가 hump + 약피크 | **새 결정상 0**: LiCl(digest d-spacing 계산: (111) 13.76°·(200) 15.9° Mo Kα)·Li₇PS₆(아지로다이트 패턴)·β-LPS 피크 **모두 없음**. 산물은 XRD-무음 → "비정질" 은 **부재 증명**이다 |
| **Raman** | Fig. S10b | PS₄³⁻ 425.8 → **420.4**(xlsx 최대; 그림 라벨 418) · **강도 0.74 → 0.095 (8×↓)** · Li₂S 370 cm⁻¹ 피크도 milled 시료에서 **소실**(창 최대 384, h 0.05) — 스펙트럼 전체가 약함 | 매우 약한 광대역 위의 어깨. PS₄³⁻ 420 부근은 **β-LPS·유리질 Li₃PS₄·과밀링 LPSCl(422)** 이 공유 → "LPS" 동정은 *배제 진단*에 가깝다. Li₂S 신호까지 사라진 것은 형광/흡수 문제 시사 |
| **XANES LCF** | Fig. 4f · Fig. S20 · Table S5 | pristine: **LPSCl 33.2 / LPS 31.2 / Li₂S 35.6** (χ² 0.050, R 0.0009); 충전: S 45.4 / LPSCl 37.6 / LPS 17.0; 방전: LPSCl 34.0 / LPS 33.3 / Li₂S 32.7 | 기준 4종뿐 — **Cl 을 품은 비정질 Li–P–S–Cl 은 LPSCl 이나 LPS 로 강제 배정**된다; SI 가 *"LPSCl and LPS … similar features"* 라고 자인. 표면 0.5–수 µm |
| **EIS** | Fig. S10c | 1 h **R ≈ 1145 Ω** → 10 h **2675 Ω** (Source Data; Ti\|composite\|Ti) — 본문 "reduction in composite ionic conductivity" | **σ 숫자·두께 미기록**. **밀링 전(mixed) 복합체 σ 미측정** → 밀링이 σ 를 *올렸는지* 알 수 없음 |
| **전기화학** | Fig. S9 · S11 · Fig. 4f | 723 mAh g⁻¹, CE 99.3 %(vs multi-step 378/252, hand-mix 0); 2 cyc 부터 충전 ~2.5–2.7 V 숄더·방전 ~2.2 V 어깨 추가, 용량 720→744 | 성능은 계면상의 **존재** 를 시사할 뿐 **전도도** 를 재는 것이 아님(1 mg cm⁻², C/20 는 느린 조건) |
| 없는 것 | — | **TEM/STEM · NMR · PDF · XPS · Ea · σ_e · LiCl 탐색 · Li₇PS₆ 고려** | |

## 7. ★4 계면상의 이온전도·Ea·전자전도 — 논문이 잰 것과 안 잰 것

- **잰 것**: 복합체 펠릿의 **총 이온전도(EIS, Ti 차단전극)** 만. S/LPSCl(σ 3점), LPSCl 단독(3점), LPS vs LPSCl(2점), Li₂S/LPSCl(**Nyquist 2점, σ 미기재**). 전부 25 °C 단일 온도 → **Ea 없음**. DC 분극 없음 → **σ_e 없음**. 계면상 단독 σ 는 어디에도 없다 — "ionically conductive interphase" 는 **복합체 σ 상승(S 계)** 과 **셀 성능(Li₂S 계)** 에서의 추론이다.
- **Source Data 로 복원한 저항과 두께 (digest 계산, A = 0.785 cm²)**
  | 시료 | R_lowf (Ω, 반원 저주파 끝) | 논문 σ | 역산 두께 L = σ·R·A |
  |---|---|---|---|
  | S/LPSCl 0.5 h / 1 h / 10 h | 10 849 / 3 145 / 3 523 | 6.0×10⁻⁶ / 2.1×10⁻⁵ / 2.0×10⁻⁵ | **0.51 / 0.52 / 0.55 mm** |
  | LPSCl pristine / 1 h / 10 h | 31.5(절편) / 38.0(절편) / 1 605 | 1.8×10⁻³ / 1.3×10⁻³ / 4×10⁻⁵ | 0.45 / 0.39 / 0.50 mm |
  | LPSCl / LPS (Fig. S8a) | 31.5 / 1 393 | 2×10⁻³ / 4×10⁻⁵ | 0.49 / 0.44 mm |
  | **Li₂S/LPSCl 1 h / 10 h** | **1 145 / 2 675** | **미보고** | — |
  두께가 0.39–0.55 mm 로 일정하므로 **같은 두께(≈0.5 mm)를 가정하면** Li₂S/LPSCl ≈ **5–6×10⁻⁵ S cm⁻¹ (1 h) / ≈2.5×10⁻⁵ (10 h)** — S/LPSCl 1 h 의 약 2.7배, 촉매전해질의 약 1/40. ⛔ **digest 추정값이다. 논문값처럼 인용하지 말 것. 우리 UMA σ 와 같은 칸에 두지 말 것.**
- **해석에서 조심할 것**: Li₂S 복합체 σ 가 LPSCl 의 1/40 이라도 셀이 723 mAh g⁻¹ 을 내는 이유는 (i) 1 mg cm⁻² · C/20 의 느린 조건, (ii) 50 wt% LPSCl 이 여전히 연속상, (iii) 75 MPa. 즉 "비정질 계면상이 전도를 살린다" 와 "비정질화돼도 벌크 LPSCl 경로가 남아 셀이 돈다" 를 이 데이터로는 **가를 수 없다**.

## 8. ★5 반응 생성물인가, 기계적 비정질화인가 — 저자 해석 vs 근거

| | 저자의 해석 | 근거로 든 것 | 근거가 실제로 가르는 것 |
|---|---|---|---|
| S 양극 | **화학반응**: *"interfacial reaction between sulfur and LPSCl … sulfur bonding between the solid electrolyte and sulfur particle"*; *"A high milling intensity is required to induce the interfacial reaction"* | TGA 미회수 S · Raman(149 / 420) · XANES edge · S:P 과잉 · **σ 상승 vs LPSCl 단독 하락** · rpm↑→이용률↑ | 가장 강한 것은 **σ 의 방향 대비**(S 가 있으면 10 h 에도 안 무너짐). 나머지는 "S 와 LPSCl 이 나노 혼합됐다" 로도 설명됨. 저자도 밀링이 *"introduces heat, breaking down sulfur rings, … distort PS₄³⁻ units, creating loose P–S bonds"*(ref 40 Gamo 2022) 라고 **기계적 경로를 같이 적는다** |
| Li₂S 양극 | **분해**("Li₂S reduces LPSCl to LPS") + 그것이 **redox-active 산물** 이라는 긍정적 재해석 | XRD 피크 소멸 · Raman 418 · LCF 절반 LPS · 2 cyc 이후 SSE-redox 숄더 | **반응 vs 기계적 비정질화를 분리한 실험이 없다**: (a) LPSCl 단독 10 h 도 같은 산물 → 순수 기계적 경로 존재; (b) Li₂S 첨가 시 1 h 에 완료 → 가속; 가속이 화학(조성이 Li₂S 쪽 → 우리 0층 hull: LPSCl 은 Li₃PS₄–LiCl–Li₂S 삼상 영역 안, 48–83 meV/atom 위) 인지 기계(경질 Li₂S 매체 효과)인지 **미판정**. Li₂S 가 소모되지 않은 것(LCF 35.6 ≈ 명목 37.5)은 "Li₂S 가 반응물" 이라는 표현과 **맞지 않고** 분해 촉진자라는 그림과 맞는다 |

**digest 판정**: 이 논문은 두 경로를 구분할 설계(예: 같은 밀링 에너지의 불활성 매체 대조군, 온도 제어, 밀링 시간별 Raman/XRD 시계열, Cl 추적)를 갖지 않는다. 우리 가설("비정질 계면층")에 대해 논문이 주는 것은 **필요조건 충족**(LPSCl 이 실제로 비정질 LPS-like 로 변한다)이지 **기구 판정**이 아니다.

## 9. ★6 "highly utilized" 가 계면상에 얼마나 의존하나 — 다른 요인과 분리됐나

| 요인 | 논문 데이터 | 분리 여부 |
|---|---|---|
| 1-step 고에너지 밀링 자체 | hand-mix 183 → multi-step 599(CE 17 %) → 1-step 1451–1615 mAh g_S⁻¹ (Fig. 2a); Li₂S: 0 → 252/378 → 720/724 (Fig. S9) | **필요조건** 확인. 그러나 1-step 은 "계면상 형성 + LPSCl 비정질화 + 나노 혼합 + 접촉" 이 **한 묶음** |
| 밀링 세기 | 300/400/500 rpm → 565/953/1615 (Fig. S3) — *"incomplete formation of the Li₃PS₄₊ₙ phase"* | rpm 별 Raman/XRD/TGA 가 **없다** → 계면상 양과 접촉 개선을 못 가름 |
| 촉매전해질 벌크 σ | LPS(0.04 mS) 1147 vs LPSCl(2 mS) 1615, 분극 0.58 vs 0.54 V (Fig. S8b) | σ 50배 차가 이용률 −29 % → **벌크 경로가 지배적 변수 중 하나** |
| 활물질 입경 | bulk 1500 / micron 1615 / sub-micron 1694 mAh g_S⁻¹ (Fig. 5d, 첫 사이클) | 첫 이용률엔 ±6 %; 율속·수명엔 큼(옆 카드) — 계면상은 세 경우 모두 생김 |
| 탄소 비표면적 | VGCF/AB/KB → 이용률(주로 SSE 몫)↑, 수명 불변 (Fig. S29) | SSE-redox 용량은 탄소 접촉이 좌우 |
| SSE 자체 용량 | LPSCl/C 단독 115/355 mAh g⁻¹; 30 wt% 셀에서 충전 용량의 **27.5 %** 가 LPSCl (Table S2) | "CE 129 %" 의 정체. **이용률 > 100 % 의 상당 부분은 계면상이 아니라 벌크 LPSCl redox** |
| 스택압 / 온도 | 펠릿 전부 75 MPa·25 °C; 파우치 10 MPa 는 **60 °C** | 압력 변주 실험 없음 |
| SE 분율 | 50 wt% 고정(10/20 wt% S 셀은 70/55 wt%); S 이용률 84 %(30 wt%) → 92 %(10 wt%) (Table S3) | SE 가 많을수록 이용률↑ — 접촉/경로 효과 |

⇒ 계면상의 **고유 기여로 논문이 계산한 몫은 방전 7.5 % · 충전 10 %**(Table S2)이고, "highly utilized" 의 나머지는 **접촉(밀링) + 벌크 LPSCl σ + LPSCl redox** 다. 계면상이 *이용률의 원인* 이라는 인과는 상관·산술 위에 있고, 요인 분리 실험은 없다.

## 10. LPSCl redox·가역성 — 계면상 서사를 떠받치는 전기화학 (Fig. 3·4·S11–S13·S16, Table S2–S5)

- **LPSCl/C 단독(80:20, Li₁In)**: 1–3 V, 20 mA g⁻¹ — 환원 **115**(plateau 1.15 V) / 산화 **355** mAh g⁻¹, 2사이클 가역 ≈ 325 (Fig. 3a). 3.5–1 V 창: 가역 ≈ 415 (Fig. S13). LPS/C: 171/312, 환원 전위 LPSCl 보다 약간 높음(Fig. S12).
- **저자 반응식(p6)**: `Li₆PS₅Cl + Li⁺/e⁻ → Li₂S + Li₄PS₄ + LiCl` (Q_red ≈ 100) · `Li₂S + Li₄PS₄ + LiCl → Li₂.₅PS₄ + S + 3.5 Li⁺/e⁻ + LiCl` (Q_ox ≈ 350) · 가역 `Li₂S + Li₄PS₄ ⇌ Li₂.₅PS₄ + S + 3.5 Li`. 완전산화 산물 S + LiCl + P₂S₅, 완전환원 Li₂S + LiCl + Li₃P(ref 26 Tan 2019, 29 Schwietert 2020). *"the high oxidative tendency of LPSCl at 2.3 V vs Li/Li⁺ is also effective at reducing the activation potential of Li₂S oxidation … 2.4 V"*.
- **CV (0.1 mV/s, Fig. 3b)**: S 셀 환원 피크 ≈1.7 V·산화 ≈2.7 V(6사이클까지 성장, ~1.5 mA cm⁻²); LPSCl 셀 산화 ≈2.5 V 성장(figure-read).
- **dQ/dV (Fig. 3c,d)**: I S⁰→S²⁻ 1.7–2.1 V(30 wt% 최대 −2300 mAh g_active⁻¹ V⁻¹ figure-read) · II SSE 환원 1.3 V(Li₃PS₄₊ₙ)·1.15 V(LPSCl) · III Li₂S 산화 2.37 V · IV SSE 산화 2.70 V. 3사이클엔 2.1–2.55 V 에 "Reversible LPS phase" 띠.
- **사이클 후 상**: XRD(Fig. 4b) 방전 = LPSCl 결정성 회복 + 나노 Li₂S + Li₃PS₄(15°); 충전 = Li₂S 소멸·비정질 S(10.5°)·LPS 15° 잔존. Raman SSE 벌크(Fig. S16): 425.8(LPSCl) + 417.3(LPS) 2피크 fit. TGA(Fig. 4c): pristine 23.4–23.7 / 방전 2.1 / 충전 19.7–19.8 %.
- **XANES LCF 사이클 추적(Table S5, 종 기준 합 100)**: LPSCl/C 방전 LPSCl 52.1 / LPS 47.9 → 충전 S 11.6 / LPSCl 60.9 / LPS 27.5; S/LPSCl/C 방전 LPSCl 45.3 / LPS 34.4 / Li₂S 20.2 → 충전 S 32.0 / LPSCl 45.1 / LPS 22.9; Li₂S/LPSCl/C 충전 S 45.4 / LPSCl 37.6 / LPS 17.0 → 방전 LPSCl 34.0 / LPS 33.3 / Li₂S 32.7. ⚠ Fig. 4d–f 막대는 패널마다 정규화 기준이 섞여 있다(합 ≈83 = 탄소 20 % 포함 복합체 기준, 합 100 = 종 기준) — **숫자는 Table S5 로**.
- **in-situ EIS (Fig. 4a, S15)**: 방전 후 전하이동저항 +85.2 Ω, 충전 후 회복.

## 11. ★7 계산 — **원자 계산 0**

DFT · AIMD · MLIP · NEB · COHP · Bader · 어느 것도 없다. "modeling" 은 전부 **연속체**: MATLAB 확률적 voxel 전극 생성(Duquesnoy 2020 코드; S 구체 + 탄소 응집체, 공극 10 vol%, S 30–60 %, LPSCl:탄소 부피비 5:2, R_S bulk 25–50 / micro 0.5–5 / nano 0.25–0.5 µm, 셀 200/50/15 µm, 3반복), **TauFactor** τ, **Iso2Mesh → COMSOL 6.1** 선형탄성 + "Hygroscopic Swelling" 등가 팽창(E_S 17.8 · E_LPSCl 22 GPa · ν 0.32/0.3 · ρ 2/1.6 g cm⁻³, β_H 22.5·24×10⁻³ m³ kg⁻¹; Table S6/S7). 상세·비판은 `cronk2026_lis_positive_electrode_geometry_fem.md` §3–5. ⚠ Methods 는 FEM 표를 "Tables S3 and S4" 라고 적었으나 실제는 **S6/S7**.

## 12. Figure set ★ (본 그림 ✓ / 안 본 그림 ✗ — §19 와 같음)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 ✗ | 개념도(계면상·SSE redox·입경·부피상쇄) | 없음(모식도) |
| 2a ✓ | 1-step / multi-step / hand-mix 첫 사이클 (1 mg_S cm⁻², C/20): 1451 / 599 / 183 mAh g_S⁻¹, 충전 1943 | "1-step 이 필요조건" 의 원자료 |
| 2b ✓ | XRD Mo Kα: 1-step 만 hump + 피크 약화(LPSCl(220) 0.70→0.15) | 비정질화 정량(§6.1) |
| 2c ✓ | Raman S–S E₂ 굽힘: 전극 149.1 vs S₈ 152.4; **milled S/LPSCl 152.4(이동 없음)** | ⚠ 본문과 어긋나는 그림 — §17 |
| 2d ✓ | XANES: 전극 2471.0 / LPSCl 2472.4 / S 2473.6(라벨), 1차미분 | "pre-edge" 의 실체 = 0.8 eV 이른 edge |
| 2e ✓ | 모식도: S 입자 껍질 Li₃PS₄₊ₙ | 저자 그림이지 관측 아님 |
| 3a ✓ | LPSCl/C 단독 115 / 355 mAh g⁻¹, 2 cyc 가역 ≈325 | 축 B/E: LPSCl redox 창 |
| 3b ✓ | CV 0.1 mV/s S 셀·LPSCl 셀 6 cyc | 산화 피크 ≈2.5–2.7 V(figure-read) |
| 3c,d ✓ | dQ/dV 1st/3rd, 영역 I–IV, 1.15 / 1.3 / 2.37 / 2.70 V | 환원 1.15–1.3 V ↔ 우리 hull 1.24 V |
| 4a ✓ | in-situ EIS OCV/1 V/3 V | 가역성 |
| 4b ✓ | XRD 사이클: 방전 시 LPSCl 결정성 회복·Li₂S·LPS 15° | 비정질화의 가역성 |
| 4c ✓ | TGA pristine 23.4 / 방전 2.11 / 충전 19.8 % | |
| 4d–f ✓ | XANES LCF 막대(정규화 혼재) | **Table S5 로 대체** |
| 5 ✗ | 기하 모델·τ·입경 전기화학·FEM 응력 | 옆 카드 정본 |
| 6 ✗ | cryo-FIB 단면·operando 압력 | 옆 카드 정본 |
| 7 ✗ | 고로딩·건식전극·파우치·에너지밀도 | 옆 카드 정본 |
| S1 ✗ | 세 공정 모식도 | 텍스트로 충분 |
| S2 ✗ | LPSCl bulk vs 밀링 후 SEM | |
| S3 ✓ | 300/400/500 rpm 첫 사이클 565/953/1615; g_active 기준 210/340/600 | 세기 의존(§9) |
| S4 ✓ | **S/LPSCl(무탄소) XRD·Raman·EIS(0.5/1/10 h) + LPSCl 단독 XRD·Raman·EIS(1/10 h)** — σ 범례 6.0×10⁻⁶/2.1×10⁻⁵/2.0×10⁻⁵; 1.8×10⁻³/1.3×10⁻³/4×10⁻⁵; LPSCl 10 h 에 Li₂S(XRD)·422 cm⁻¹·P₂S₆⁴⁻ | **이 카드의 핵심 그림 ①** — 과밀링 창 |
| S5 ✓ | TGA 1-step 전극: S₈ 23.5 %, "S_reacted 6.5 %" | 미평탄 곡선(§17) |
| S6, S7 ✓ | cryo-TEM·HAADF·EDS 맵·라인스캔(입자 1·2) | 투영 한계(§6.1) |
| S8 ✓ | LPS 0.04 vs LPSCl 2 mS cm⁻¹; S 셀 1147 vs 1615 | 벌크 σ 의 몫(§9) |
| S9 ✓ | Li₂S 세 공정: 724/720 · 378/252 · ≈0 | **우리 계의 필요조건** |
| S10 ✓ | **Li₂S/LPSCl XRD·Raman·EIS** — 아지로다이트 피크 소멸·Li₂S 잔존·418 cm⁻¹·R 1145→2675 Ω | **이 카드의 핵심 그림 ②** |
| S11 ✓ | Li₀.₅In\|LPSCl\|Li₂S 1–5 cyc: 숄더 추가·용량 720→744 | SSE redox 산물이 합성 중 생김 |
| S12 ✓ | LPS/C vs LPSCl/C 첫 사이클 171/312 vs 115/355 | 환원 전위 순서(dQ/dV II 배정 근거) |
| S13 ✓ | LPSCl/C 3.5–1 V: 가역 ≈415 | Li₂S 창에서의 SSE 용량 |
| S14 ✗ (xlsx 로 대체) | 사이클 후 S–S 굽힘 150.2(5·100 cyc) | 계면상 보존 |
| S15 ✗ | Fig. 4a 등가회로·fit | |
| S16 ✓ | SSE 벌크 Raman 2피크 fit 425.8 + 417.3 | 전기화학적 LPS 생성 |
| S17–S20 ✗ | XANES 기준 스펙트럼·LCF 피팅 곡선 | Table S5 로 대체 |
| S21–S22 ✗ | XRD/XANES 용 셀 전기화학 | |
| S23–S27 ✗ | S·Li₂S 분말 SEM·EDS·입경 XRD | 옆 카드 |
| S28–S31 ✗ | 입경별 2사이클·율속·탄소종·EIS fit·단면 | 옆 카드 |
| S32–S35 ✗ | 부피팽창 추정·표면 균열·μSi\|\|Li₂S 풀셀 | 옆 카드 |
| Table S1 (텍스트) | STEM 맵 정량 (S 68.7 / P 7.8 / Cl 6.9 / O 16.7 at%) | §6.1 |
| Table S2 ✓(이미지) | 용량 기여 산술 — 방전 83.3 / 7.5 / 9.2 %, 충전 62.1 / 10 / 27.5 % | §9 |
| Table S3 (텍스트) | 10/22/30 wt% S 이용률 92 / 84.3 / 84 % | §9 |
| Table S4 (텍스트) | TGA 10 mAh cm⁻² 전극 20 / 93.1 / 34 % reacted | §6.1 |
| Table S5 ✓(이미지) | XANES LCF 9행(χ²·R-factor 포함) | **§6.2·§10 의 정본 수치** |
| Table S6–S8 (텍스트) | FEM 파라미터·식·에너지밀도 입력 | 옆 카드 |

## 13. Post-processing / 도구 (논문)

- XRD: Bruker ApexII-Ultra CCD 회전양극 **Mo Kα 0.7107 Å**, 0.7 mm 붕소 모세관 밀봉, 5–50° 2θ (⚠ Cu Kα 환산 시 2θ 약 2.2배).
- Raman: Renishaw inVia, **785 nm**, Kapton 밀봉 슬라이드. 피크 fit(Fig. S16) 도구 미기재.
- XANES: TLS 16A1, Si(111) DCM, **TFY Lytle**, 0.2 eV step, S₈ 2472 eV 보정(1차미분 최대), **Athena** LCF(비선형 최소제곱; 기준 S·LPSCl·LPS·Li₂S).
- TGA: NETZSCH STA 449 F3, Al 팬 크림프, N₂, 5 °C/min → 450 °C.
- (S)TEM: Talos X200, 200 kV, 저선량, cryo(~−180 °C), Super-X EDS 4검출기, Melbuild 밀폐 홀더.
- EIS: Biologic SP-300, 30 mV, 7 MHz–100 mHz, 10 pt/dec, σ = L/(R·A), ZView.
- 연속체: MATLAB(기하) · TauFactor · Iso2Mesh · COMSOL 6.1(옆 카드).
- 수치화·기록: Source Data xlsx 30 시트(그림별 원시 곡선; ⚠ 시트명 S15–S19 가 출판 SI 번호와 **1씩 어긋남**: xlsx "Fig. S15" = 출판 Fig. S16 … xlsx "Fig. 19" = 출판 Fig. S20); figshare 10.6084/m9.figshare.31094524(FEM 응력).

## 14. ★ 우리 0층 열역학과의 대조 (`db/properties/lpscl_li2s_hull_layer0_2026_09_11.json` · prereg 카드)

| 우리 결과 (2026-09-11) | 이 논문의 관측 | 맞는 곳 | 갈리는 곳 / 방법 의존성 |
|---|---|---|---|
| **① 0 K hull: Li₂S–Li₆PS₅Cl 사이 안정 중간 결정상 없음** — 분해 산물 {Li₃PS₄, LiCl, Li₂S} 가 x 전 구간 동일 (UMA + MP-DFT 교차, ⚠ post-hoc) | 볼밀 Li₂S/LPSCl(x = 0.778): **새 결정상 0**, 아지로다이트 피크 소멸, Li₂S 잔존, P 는 "LPS(Li₃PS₄)-like" 로(Raman 420·LCF 48 %) | ✅ **정성 일치** — 평형 산물의 P 부분(Li₃PS₄)이 실험에서 나타나고 새 상은 없다 | 실험 산물은 **XRD-무음(비정질)** 이고 우리 ① 은 결정 평형. **LiCl 은 관측·언급 0** → ① 의 Cl 부분은 검증 안 됨(비정질 Li–P–S–Cl 에 남았을 수도, 나노 LiCl 일 수도). 논문 조건(500 rpm 1 h, 25 °C 근방 국소가열)은 비평형 |
| **② 준안정층: Li₆PS₅Cl + Li₂S → Li₇PS₆ + LiCl, −38.4 meV/atom** | 결정 Li₇PS₆ 는 아지로다이트 패턴이므로 "피크 소멸" 과 **양립 불가** → 결정형 Li₇PS₆ 는 이 조건에서 **생기지 않았다**. Li₇PS₆ 언급 자체가 0 | — | ② 는 **반증도 지지도 아님**: 비정질 Li₇PS₆-like 국소환경은 XRD 로 배제 못 하고, Raman PS₄³⁻ 위치만으로는 LPS/LPSCl/Li₇PS₆ 를 가르기 어렵다(우리가 확인할 항목). LCF 기준에 Li₇PS₆ 가 없어 XANES 도 못 본다 |
| **③ 결정 Li₇PS₆ 는 LPSCl 보다 느리다(de Klerk 2016) → 비정질 경로만 열려 있다** | 비정질화된 Li₂S/LPSCl 은 **σ 미보고**(R 1145 Ω → 10 h 2675 Ω), 셀은 723 mAh g⁻¹·CE 99.3 %; S/LPSCl 은 1 h 밀링에 σ 3.5×↑ | 🔶 **미검증(공백)** — "비정질 경로가 실제로 통한다" 를 논문이 재지 않았다 | 논문이 주는 것은 *작동 가능성* 과 *과밀링 창(1 h 는 되고 10 h 는 나쁨)* 뿐. Ea·σ_e·계면상 단독 σ 없음. ⛔ digest 추정 σ(≈5×10⁻⁵)를 우리 UMA σ(절대값 인용 금지)와 나란히 두지 말 것 |
| 조성 지정점 x = 0.778 (3:5 wt) | 논문 30:50 wt = x 0.778 | ✅ **같은 점** — 실험 대조가 직접 가능 | 그들은 탄소 20 wt% 포함(우리 모델엔 없음), 75 MPa |
| 산화 onset 2.14 / 2.256 V(grand-potential, 축 B①) | dQ/dV SSE 산화 시작 2.70 V, 본문 "2.3 V", CV ≈2.5 V | ✓ 산물(S + LiCl + Li₃PS₄ 중간체) 정합 | 실측 kinetic onset(탄소 20 wt%, 과전압) vs 0 K 열역학 — **0.1–0.5 V 차를 실차이로 읽지 말 것** |
| 환원 계단 1.24 V(+5 Li·P) · 0 V Li₃P + 5Li₂S + LiCl | dQ/dV 환원 1.15 V(LPSCl)·1.3 V(Li₃PS₄₊ₙ); 식 `→ Li₂S + Li₄PS₄ + LiCl` | ✓ 첫 단계 전위·산물 정합(0.1 V 이내) | 1 V 컷오프라 Li₃P 단계 미관측 |
| band gap / 기계 / ε∞ | 없음 | — | 이 논문은 축 C·D 에 값을 주지 않는다(FEM 입력 E 22 GPa 는 옆 카드) |

**정직한 요약**: 논문은 우리 ① 을 *비정질 형태로* 재현하고(P → Li₃PS₄-like, 새 상 없음), ② 의 결정형을 배제하며, ③ 은 **건드리지 않는다**. 우리 1층(melt-quench 비정질 계면)과 2층(Ea 비교)이 답해야 할 질문이 그대로 남아 있고, 이 논문은 그 질문이 실험적으로 **아직 열려 있음**을 확인해 준다.

## 15. 적용 인사이트 (우리 캠페인에)

1. **가설의 출처를 정확히 달자**: "이온전도를 살린다" 는 S/LPSCl 서사(σ 6×10⁻⁶ → 2×10⁻⁵)에서 온 문장이다. Li₂S/LPSCl 에 대해 Cronk 가 보여준 것은 "비정질 LPS-like 로 분해돼도 셀이 돈다" 까지 — 우리 원고·카드에서 이 논문을 인용할 때 **문장을 Li₂S 계로 옮겨 쓰면 오인용**이다.
2. **1층(비정질 계면) 모델의 조성 후보가 좁혀졌다**: 실험 산물은 (a) 아지로다이트 골격 상실, (b) PS₄³⁻ 보존(Raman 420), (c) Li₂S 미소모, (d) Cl 행방 불명. → 후보는 **Li₃PS₄-like 비정질 + Cl 을 품은 형태(비정질 Li₃PS₄·xLiCl)** 와 **나노 LiCl 분리** 둘. 1층 melt-quench 에서 두 조성을 모두 던지고 PS₄³⁻ 보존 여부를 판정 지표로 삼을 것.
3. **2층 보고량은 "Ea(비정질 LPS-like) vs Ea(LPSCl)"** — 논문에 Ea 가 없으므로 우리 계산이 문헌 공백을 채우는 자리다. 단 실험 대조점은 "R 1145 Ω @0.5 mm 가정" 수준이라 정량 비교는 불가 — **방향(비정질화가 σ 를 얼마나 깎는가)** 만 겨눈다.
4. **과밀링 창을 우리 실험 파트너에게 전달**: 500 rpm 1 h 는 되고 10 h 는 R 2.3× 상승 · LPSCl 단독은 σ 45× 붕괴 — 볼밀 조건은 이 창 안에서.
5. **Cl 추적이 실험의 가장 값싼 다음 한 수**: Cl K-edge XANES / ³¹P·⁷Li NMR / PDF 가 이 논문에 없다. 우리 쪽 실험이 하나만 한다면 LiCl 결정 유무(Cu Kα 30–35°)와 ³¹P NMR 이다.

## 16. 인용 가능 문장 (deck/paper 용, 방어 가능한 형태)

- "Cronk et al. showed that one-step high-energy milling (500 rpm, 1 h) of Li₂S with Li₆PS₅Cl amorphizes the argyrodite — its diffraction peaks vanish while Li₂S remains crystalline — and converts about half of it into a Li₃PS₄-like environment (S K-edge LCF: LPSCl 33 / LPS 31 / Li₂S 36 wt%), yet the composite still delivers 723 mAh g⁻¹ at C/20 with 99.3 % Coulombic efficiency." (Fig. S10, Table S5, Fig. S9)
- "The composition of the amorphized interphase was not resolved: no NMR, PDF, or XPS was reported, LiCl was not detected or discussed, and the composite's ionic conductivity was shown only as Nyquist plots without a value." (Fig. S10c)
- "For sulfur–LPSCl composites the same milling raised the composite conductivity from 6×10⁻⁶ to 2×10⁻⁵ S cm⁻¹ after 1 h, whereas LPSCl milled alone for 10 h collapsed to 4×10⁻⁵ S cm⁻¹ with Li₂S and Li₃PS₄ segregation — defining a processing window." (Fig. S4c,f)
- ⛔ 쓰지 말 것: "Cronk 가 Li₂S/LPSCl 계면의 비정질상이 이온전도를 높인다고 보였다" — 논문에 없는 문장이다.

## 17. 주의 · 한계 · 본문↔데이터 불일치 (over-claim 방지)

1. **Raman "redshift" 의 범위**: 본문(p4)은 milled S/LPSCl **과** 1-step 전극 둘 다 적색이동이라 하지만 Source Data 최대값은 milled S/LPSCl **152.4 = S₈**, 전극만 **149.1**. Fig. 2c 에서도 milled 곡선은 점선 위에 있다. → Li₃PS₄₊ₙ 의 Raman 증거는 **탄소 포함 시료 1개**에 의존.
2. **XANES pre-edge 2470.1 eV**: 그림 라벨·Source Data 1차미분 극대는 **2471.0**. 게다가 이는 별도 피크가 아니라 LPSCl 보다 0.8 eV 이른 **주 edge** 이고, S₈(2466 부터 상승)과의 혼합만으로도 설명된다. 폴리설파이드형 "pre-edge" 라 부르기엔 약하다.
3. **TGA 미회수 6.5 wt%**: 450 °C 에서 곡선이 평탄하지 않다(−0.055 %/°C). 승화가 덜 끝났다면 "반응 S" 는 더 작다 → **상한**. 같은 양이 Fig. S5 23.5 · Fig. 4c 23.4 · Table S4 23.7 % 로 세 값.
4. **STEM "double"**: S:P 6.8–8.8 vs 5 → 1.4–1.8배. 투영 시료·O 17–20 at% 미설명·코어–셸 대비 부재. Li₂S 계 TEM 없음.
5. **Li₂S 복합체 σ 미보고 + 밀링 전 σ 미측정** → "비정질화가 전도를 살린다/깎는다" 어느 쪽도 이 논문으로 정량 주장 불가. 본문 자체가 한 곳에선 "reduction", 다른 곳에선 "retains" 라고 쓴다.
6. **"Li₂S reduces LPSCl"**: 산화수 변화 없는 분해. LPSCl 단독 과밀링도 같은 산물. Cl 행방 미보고.
7. **Fig. 4d–f 정규화 혼재**(합 83 vs 100) — 본문 "32 wt% sulfur after charge" 는 종 기준(Table S5), 막대는 ≈27(복합체 기준). 수치는 Table S5 로.
8. **CE 129 %**: Source Data 로는 Fig. 2a 1943/1451 = 134 %, Fig. S3a 1923/1615 = 119 %, Fig. S8b 2176/1615 = 135 % — 129 % 를 재현하는 시트가 없다(다른 셀일 수 있음).
9. **LCF 기준 집합의 한계**: Li₃PS₄₊ₙ · Li₇PS₆ · Cl-함유 비정질 기준이 없어 그 상들은 원리적으로 **검출 불가**; LPSCl/LPS 유사성은 SI 가 자인. χ² 0.24(pristine S/LPSCl/C)는 표에서 최악.
10. **미기록 파라미터**: 복합체 밀링 볼 크기/개수/용기, 무탄소 S/LPSCl 조성비, 펠릿 두께(역산 0.39–0.55 mm), Li₂S/LPSCl XRD·Raman 시료의 밀링 시간.
11. **오기**: Methods 의 FEM 표 "Tables S3 and S4" → 실제 S6/S7; 본문 "Figure 28a" → Fig. S28a; xlsx 시트 번호 S15–S19 가 출판 SI 와 1 어긋남; inbox 파일명 "Bai2026".
12. **조건 의존성**: 모든 펠릿 75 MPa·25 °C, 활물질 1 mg cm⁻²·C/20 에서의 이용률이다. "low stack pressure 10 MPa" 파우치는 **60 °C**.
13. **저자 이해관계**: LGES 공동 자금·특허 2건 — 결론의 방향(공정 단순화·촉매 불필요)이 상업적 서사와 겹친다.

## 18. 기술 미니-용어집

- **Li₃PS₄₊ₙ (lithium polysulfidophosphate)** — PS₄³⁻ 말단 S 에 S 사슬이 붙은 S-풍부 티오포스페이트(Lin 2013, Angew 52, 7460). 이온전도성·전기화학 활성. 이 논문에서는 n 을 분광이 아니라 용량으로 추정.
- **1-step vs multi-step milling** — 활물질·탄소·SE 를 한꺼번에 고에너지 밀링 vs 활물질+탄소만 밀링 후 SE 손혼합. 전자만 SE 가 밀링 에너지를 받는다.
- **S K-edge XANES / LCF** — 2470–2480 eV 흡수단으로 S 산화상태·환경 판별; LCF 는 기준 스펙트럼의 선형결합으로 분율 추정(기준에 없는 상은 못 본다). TFY 는 자기흡수·표면 민감.
- **dQ/dV 영역 I–IV** — I S⁰→S²⁻ 환원, II SSE 환원(1.3 V Li₃PS₄₊ₙ · 1.15 V LPSCl), III Li₂S 산화(2.37 V), IV SSE 산화(≥2.70 V).
- **"reacted sulfur"** — TGA 에서 450 °C 까지 승화하지 않은 S. 결합 형태와는 무관한 조작적 정의.
- **catholyte** — 양극 복합체 안의 SE(여기선 마이크론 LPSCl). 분리막 LPSCl 과 구분.
- **R_lowf** — Nyquist 반원의 저주파 끝 실수부(digest 용어). 저자는 σ = L/(R·A) 로 σ 를 냈고 어떤 R 을 썼는지 미기재; 역산 두께가 일정한 것으로 보아 반원 끝을 쓴 듯.

## 19. 본 그림 / 안 본 그림 (2026-09-11)

- **크로핑**: `litdb/figures/cronk2026_lis_cathode_interphase_chemistry/` 50장(본문 7 + SI 35 + 표 8). 자동 크롭이 **Fig. 3(오른쪽 열 3b·3d 누락)·Fig. 4(4c 절단·4f 누락)** 을 놓쳐 **수동 bbox 로 재렌더**(figures.json `note`).
- **실제로 본 것 (17/50)**: fig_2 · fig_3(재크롭) · fig_4(재크롭) · fig_S3 · S4 · S5 · S6 · S7 · S8 · S9 · S10 · S11 · S12 · S13 · S16 · tab_S2 · tab_S5 (표 2장은 SI 텍스트 추출이 비어 이미지로 읽음).
- **안 본 것**: fig_1 · 5 · 6 · 7(옆 카드 영역) · S1 · S2 · S14(xlsx 로 대체) · S15 · S17–S35 · tab_S1·S3·S4·S6·S7·S8(텍스트로 읽음).
- **그림이 본문과 어긋난 것**: Fig. 2c(milled S/LPSCl 이동 없음) · Fig. 2d(2471.0 vs 본문 2470.1) · Fig. 4d–f(정규화 혼재) · Fig. S10c(σ 값 없음인데 본문은 "reduction" 서술).
- **figure-read 값**: CV 피크 위치(≈2.5/2.7 V), dQ/dV 30 wt% I 피크 높이, Fig. 2b 피크 위치는 xlsx 로 확인했으므로 figure-read 아님.

## 20. Source Data 시트 목록 (30) 과 전사 여부 — 전사본은 `litdb/inbox/104_source_data/`(gitignore), 저장소 내 파생 요약표는 `figures/<slug>/source_data_derived.csv`

| 시트 | 내용 | 전사 |
|---|---|---|
| Fig. 2a-d | 전압곡선 3 · XRD 3 · Raman 4 · XAS 3 + 미분 3 | ✅ `litdb/inbox/104_source_data/cronk2026_source_fig2.csv` (저장소 밖) |
| Fig. 3 | 3a 전압 · 3b CV · 3c/3d dQ/dV | ✗ (목록만) |
| Fig. 4 | 4a EIS · 4b XRD · 4c TGA | ✗ |
| Fig. 5 · Fig. 6 · Fig. 7 | 기하/τ/입경/EIS/압력/고로딩/파우치 | ✗ (옆 카드 영역) |
| Fig. S3 | rpm 별 전압곡선 | ✅ `…/104_source_data/cronk2026_source_figS3.csv` (저장소 밖) |
| Fig. S4 | S/LPSCl·LPSCl 단독 XRD·Raman·EIS | ✅ `…/104_source_data/cronk2026_source_figS4.csv` (저장소 밖) |
| Fig. S5 | TGA | ✅ `…/104_source_data/cronk2026_source_figS5.csv` (저장소 밖) |
| Fig. S6c and S7c | EDS 라인스캔 | ✅ `…/104_source_data/cronk2026_source_figS6c_S7c.csv` (저장소 밖) |
| Fig. S8 | LPS/LPSCl EIS · 셀 | ✅ `…/104_source_data/cronk2026_source_figS8.csv` (저장소 밖) |
| Fig. S9 · S10 · S11 · S12 · S13 | Li₂S 공정 · Li₂S/LPSCl 특성 · Li₂S 사이클 · LPS vs LPSCl · LPSCl Li₂S 창 | ✅ 각각 `…/104_source_data/cronk2026_source_figS9/S10/S11/S12/S13.csv` (저장소 밖) |
| Fig. S14 · S15(=출판 S16) · S16(=S17) · S17(=S18) · S18(=S19) · Fig. 19(=S20) | 사이클 후 Raman · 2피크 fit · XAS 기준 · LCF 곡선 3종 | ✗ (수치는 §3·§6 에 요약) |
| Fig. S21 · S22 · S27 · S28 · S29 · S32 · S33 · S35 | 셀 전기화학·입경 XRD·율속·탄소·부피 추정·풀셀 | ✗ |

## 21. 한 줄 결론

**LPSCl 을 Li₂S 와 500 rpm 1 h 로 갈면 아지로다이트가 사라지고 P 는 Li₃PS₄-like 비정질 환경으로 간다 — 논문이 확실히 보여준 것은 여기까지이고, 그 계면상의 조성(Cl 행방)·Ea·전도 기여는 비어 있다.** 우리 0층 ① 과는 정성 일치, ② 는 결정형 배제, ③ 은 미검증 — 1층(비정질 조성 후보 2종)·2층(Ea 비교)이 채워야 할 자리가 이 논문으로 오히려 선명해졌다.

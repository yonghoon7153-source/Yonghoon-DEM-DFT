---
name: research_profile
version: 0.2.0
updated: 2026-09-04
status: FILLED (by Claude Code, 2026-09-04)
description: 관련도 판단과 심층 분석 프롬프트에 주입되는 '내 연구' 기준 문서. 이 파일 하나만 고치면 에이전트의 판단 기준이 바뀐다.
filled_from:
  - branch claude/friendly-meitner-lldvar @ f6194e2cf (2026-09-03)
  - branch claude/stoic-knuth-NObVQ @ 047746866 (2026-09-03)
  - "두 브랜치는 git merge-base 가 없다 (unrelated histories). 억지로 합치지 않았다."
---

# 연구 프로필

> 이 파일은 위 두 브랜치의 **실제 코드·원고·db·커밋**을 읽고 채웠다. 근거가 없는 칸은 `unknown` 으로 남겼다.
> 추측으로 메우지 않았다.

## 확정된 것 (사용자 발언 근거)
- 분야: 황화물계 all-solid-state battery (ASSB)
- **연구 축은 두 개이며 서로 별개로 진행된다**
  - 축 A: DEM / MPM / voxelization
  - 축 B: DFT / MLIP
  - 두 축을 "DFT→MLIP→DEM→FEM" 같은 하나의 multi-scale 파이프라인으로 엮어 서술하지 말 것
- 추적 키워드: `dem battery`, `dft battery`

> **repo 로 확인한 결과 — 사용자 정정이 맞다.** 두 축은 별개 브랜치에 있고 git 상 **공통 조상이 없다**
> (`git merge-base` rc=1). 코드·파이프라인·실행 환경을 공유하지 않는다.
>
> 다만 **접점이 넷 있다. 전부 "번호 하나" 단위이지 자동 연결이 아니다** — 이것을 파이프라인으로
> 서술하면 안 되는 이유가 여기 있다. 한쪽 출력이 다른 쪽 입력으로 **흘러가지 않고**, 사람이
> 값 하나를 골라 옮겨 적는다:
> 1. **탄성 상수** — 축 B 의 DFT 값(E_VRH 22.06 / 27.66 GPa · B₀ 26.23 GPa · ν 0.360 · μ 8.11)이
>    축 A 의 DEM/MPM 물성 카드에 **인용**돼 있다 (축 A CLAUDE.md L568·L1131–1141).
>    ⚠ 축 A 는 그 값을 그대로 쓰지 않는다 — DEM 은 E_SE 를 **1.35 GPa 로 18× 연화**해서 쓴다.
>    DFT 값은 "실-bulk 축" 의 참조일 뿐이다.
> 2. **SDCP** — 같은 물질이 양쪽에 있다. 축 B 는 LiNiO₂(104) 위 **흡착에너지**를 계산하고(C-12),
>    축 A 는 전극 안 **전도성 첨가제**(σ_SDCP 250 mS/cm)로 넣는다. 축 A 의 SDCP 캠페인은
>    `잔여 = E_bind DFT` 로 **축 B 의 값을 기다리는 중**이다 (`[[anchor-waitlist]]`).
> 3. **litdb** — 논문 카드 정본은 **축 B 브랜치의 `litdb/` 하나뿐**이다(2026-07-16 결정).
>    축 A 의 `litdb/` 는 동결 스냅샷이며 추가·수정 금지. 새 카드는 축 B 브랜치에만 넣는다.
> 4. 공저자용 Methods .docx 를 양쪽이 각각 낸다 (v7 / v8). 같은 원고인지는 **unknown**.
>
> ⇒ 정확한 서술: **두 개의 독립 연구 프로그램이 재료(SDCP·LPSCl)와 문헌 서랍을 공유한다.**
> "DFT→MLIP→DEM→FEM 다중스케일 파이프라인" 은 틀렸다.

---

## 축 A (DEM / MPM / voxelization) — 브랜치 `claude/stoic-knuth-NObVQ`

**한 줄**: 황화물 복합양극을 **DEM(LIGGGHTS)과 MPM(Taichi GPU) 두 독립 모델**로 압밀하고,
각각에서 나온 미세구조 위에서 **접촉망 Kirchhoff σ** 와 **복셀 유한체적 σ** 두 개의 독립
수송 해를 구한 뒤, 그것을 전기화학(BV/CV 시간전개)까지 밀어 ASR·율특성을 낸다. 그리고 그
결과를 **물리로 구조화된 회귀(스케일링 법칙)** 로 압축해, 설계 수치 → 물성 → 2D 미세구조
합성까지 가는 예측기를 만든다.

> ⛔ **이 축의 통제 인식론 (frame[4], FINALIZED 2026-06-07)** — DEM 과 MPM 을 **서로 보정하지
> 않는다.** 각자 실험에만 독립 보정하고 결과를 비교한다. 일치 = 교차검증, 불일치 = 정량화된
> 모형 한계(정보이지 실패가 아니다). 한쪽을 다른 쪽에 맞추는 것은 순환논증이다.
> ⇒ 문헌을 읽을 때도 "DEM 과 FEM/MPM 을 서로 캘리브레이션했다" 는 논문은 **방법론적으로
> 우리와 반대**이며, 그 점이 비판 포인트다.

### 파이프라인 (축 A 내부 — 이건 하나의 파이프라인이 맞다)
```
STEP1 DEM (LIGGGHTS)  →  STEP2 MPM 압밀/payload  →  STEP3 복셀 σ (∇·σ∇φ=0)  →  STEP4 전기화학
  패킹·접촉·force chain    소성 형상·void-fill·응력장    σ_ion·σ_e·k_thermal      비선형 BV+구형확산
  Auerbach 파괴            (mpm3d_compaction.py)        (step3_sigma.py)         (step4_dyn.py)
                                                                                  → STEP6 surrogate
```
⚠ **σ 를 내는 솔버가 둘이고 파이프라인이 다르다** — `scripts/network_conductivity.py`
(DEM 접촉망 · Holm 협착 · **웹앱** 경로) 와 `scripts/voxel_conductivity.py`·`step3_sigma.py`
(MPM 복셀 FV · **킷 `run_mpm.sh`** 경로). 한쪽이 다른 쪽의 근사가 아니라 **다른 이산화의
독립 측정**이다. 웹앱 코드리뷰 수정이 STEP3 에 자동 적용되지 않는다.

### 쓰는 도구·코드 (repo 경로 · 크기순)
- `scripts/generate_comparison_plots.py` (376 KB) — 스케일링 법칙 전역 적합의 본체
- `scripts/mpm3d_compaction.py` (300 KB) · `scripts/mpm2d_*.py` (8개) · `mpm_webapp_payload.py` (233 KB) — MPM
- `scripts/step4_dyn.py` (228 KB) — 전기화학 시간전개 · `step4_pybamm_anchor.py` — PyBaMM 대조
- `scripts/step3_sigma.py` (220 KB) · `voxel_conductivity.py` — 복셀 수송
- `scripts/sdcp_gain_verdict.py` (201 KB) — SDCP 이득 판정기
- `scripts/check_method_discipline.py` (185 KB) — 방법 규율 자동 점검
- `scripts/network_conductivity.py` (85 KB) — DEM 접촉망 Kirchhoff · `run_network_full_corrections.py` — Stage E
- `scripts/ml_design_structure.py` · `webapp/predictor_engine.py` · `structure_predictor.py` — 설계→구조 ML
- `scripts/extract_2d_microstructure.py` (69 KB) — **2D 미세구조 합성**(voxelization 산출)
- `scripts/grade_engine.py` (86 KB) — 파생 지표 ~30종 · `build_comsol_mph.py` (93 KB) — COMSOL
- `scripts/electronic_nested_cv.py` · `thermal_regression.py` · `nested_cv_sat.py` — 모형 선택
- `dem_scripts/*.liggghts` · `heckel/input_SE_heckel_{100..400}.liggghts` — DEM 입력
- `se_curve/xfer_kit_ps_*.json` — P:S 조성별 대조군 침대 전송킷
- `webapp/app.py` — Flask 케이스 브라우저 + 3D 뷰어 · `wiki/` (21페이지, `wiki/tools/lint.py`)
- `scripts/` 총 **490개** (screening 53 · physics 29 · plot 25 · electronic 20 · thermal 15 · sr01 12 …)

### 대상 시스템
- AM **NCM811** bimodal (AM_P 대입자 poly / AM_S 소입자 single-crystal, 반경문턱 3.5 µm)
- SE **Li₆PS₅Cl** · 첨가제 **VGCF · SuperP · PTFE · SDCP**(전도성 고분자, σ_SDCP 250 mS/cm 규약)
- 조성 축 `am_wt`/`se_wt` · P:S 비 0:10 ~ 10:0 · 압력 100–400 MPa · SBE/DBE(단일/이중 바인더)
- 실험 협업계: AM:SE:VGCF:PTFE = **80:18:1:1**, 4 µm single-crystal(No.1/No.2), poly:small 5:5

### 관심 물리량과 현재 확보된 값
| 양 | 값 / 범위 | 출처 |
|---|---|---|
| porosity | 15.0 – 19.7 % | `all_dem_porosity.csv` (80케이스) · `docs/db/section7_10case_sweep.csv` |
| σ_ionic | 0.117 – 0.173 mS/cm | 같은 CSV |
| σ_electronic | 3.18 – 4.63 mS/cm | 같은 CSV |
| σ_thermal | 3.42 – 4.33 mS/cm | 같은 CSV |
| percolation | 92.3 – 99.7 % | 같은 CSV |
| 배위수 CN | AM–AM 2.73–3.86 · SE–SE 4.39–5.24 | 같은 CSV |
| τ_Laplace | 1.21 – 4.39 | 같은 CSV |
| 접촉력 F_DEM | 1.32 – 9.04 mN | 같은 CSV |
| Heckel (DEM pure-SE) | R² 0.965 · P_y 138 MPa · σ_y_eff 46 MPa | CLAUDE.md frame[3] |
| MPM 보정값 | E_eff 1.53 GPa · σ_y 0.15 GPa (2D) · pure-SE 항복 ≈86 % | frame[1] |
| DEM 보정값 | E_SE 24 → **1.35 GPa (18× 연화)** | `docs/esse_calibration_2mAh_real_9.md` |
| Furnas dip | AM 75–85 wt% (DEM 전용 — MPM 은 재현 못 함) | frame[3]·CORRECTION 2 |
| 2C CCCV (SBE→DBE) | delivered 88.9 → **89.6 %** · CC ΔV 9.3 mV(옴 4.5 + kin 4.8) | 원장 §5.5 |

**스케일링 법칙 (production form, 전부 FINALIZED)** — 이게 이 축의 헤드라인 산출물이다:
- **σ_ionic** (2026-05-28) LOOCV **0.9752** · n=90/k=5 (18:1)
  `σ = σ_grain·Cronau(r_SE)·φ_eff^½·CN²·cov_Hertz^½·f_p³·exp[a+b·lnτ+c·(lnτ)²+β_P2·P2+β_F·log f_intact]`
  (σ_grain 3.0 mS/cm · φc_P 0.200 · φc_S 0.195 · δ 0.040 · r_cut 3.5 µm · α 2 — 전부 FROZEN)
- **σ_electronic** Stage 22.5 (2026-06-03) LOOCV **0.9531** · R² 0.9613 · 8 LIVE OLS + 2 LOCKED (9.5:1)
- **σ_thermal** Stage T1 (2026-06-04) LOOCV **0.9028** · R² ≈0.96 · Ridge α=0.05 · 14 feature (6:1)

### 방법론적 쟁점
- **frame[4] 교차보정 금지** (위 ⛔ 참조) — 이 축의 제1 규율
- E_SE 18× 연화가 무엇을 뭉뚱그리는가 (재배열·GB 미끄러짐·미세파괴) · Hooke vs Hertz 등가성
- Auerbach + **Lawn** 단계별 파괴 · Stage E grain 보정 (Cronau 2021/22 · Trevisanello 2021 · Wang 2022)
- high-contrast Laplacian → **7층 방어** · **Bruggeman EMT** 가 왜 건전한 상한인가
- **격자(voxel) 수렴** — SR-01 의 핵심. vox 0.4→0.15 µm 에서 σ_e 이득이 **단조 증가하며 멈추지 않고**,
  증분비 1.773 < 이론 하한 2.187 이라 **멱법칙 수렴이 성립하지 않는다** ⇒ Richardson 외삽 무의미.
  이 하드웨어 한계 = vox 0.115 µm (peak RSS 35.6 GB)
- **표현 부피** 문제 — 점 스탬프가 섬유를 20.6–75.8 % 조각내고, SDCP 표현부피/참부피가 격자에 따라
  0.238 ~ 4.311 배(18.1배 변동). `--step3-sdcp-sphere-d` 로 참 직경 구 스탬프 신설
- 준정적 게이트 `V/c_P ≤ 0.01` — 위반 런은 등급 B(상대비교 전용)
- **n/k 비율 규율** · "정보이론적 천장 — 항을 더 넣지 마라"
- 사전등록(`docs/reviews/*_prereg_*.md`) · 인용금지 목록(`claims.json` `quotation_ban`)

### 진행 중 / 끝난 것
- **끝**: Phase 1 수송 삼중(σ_ionic/σ_e/σ_thermal) · frame[4]/[5] 확정 · E_SE 보정 · Heckel ·
  80–82케이스 porosity 검증 · STEP4-v2 구현 · 2C CCCV 완주 · bimodal R_ct 원장
- **진행**: 원고 `docs/paper/main.tex` 공저자 편집 시트 · SR-01 격자 수렴(미해결) ·
  LHS 스윕 8개 · SDCP 전도도 판별 팔 · litdb 흡수 CL-60~65 · R_int 풀셀/사이클 Phase 2
- **대기 앵커** (`[[anchor-waitlist]]`): Joule ΔT · 코팅 √N · **SDCP E_bind (← 축 B 의 DFT)** ·
  NCA E175 · EIS C_dl/R_w
- **큰 목표(사용자 비전)**: 설계 수치 입력 → ML 이 전 물성 예측 → 그 수치에 맞는 2D 미세구조를
  그리고 → 최종적으로 서로 다른 구성을 **한 복합양극 안의 층**으로 쌓는다 (5단계 중 Phase 1 완료)

### 이 축과 무관한 논문의 특징 (오탐 감축용)
- 원자 스케일 전용 계산 (DFT 밴드구조 · NEB 장벽 · AIMD) — **그건 축 B 다**
- 액체 전해질 슬러리 코팅·건조, 파우치셀 사이클 수명만 보고하는 실험
- 셀 레벨 BMS·열관리·팩 설계, SOC/SOH 추정, 전산유체(CFD)
- 순수 합성·소결 (미세구조 정량이나 수송 측정 없이 XRD·SEM 사진만)
- 상평형·CALPHAD · 전극 없는 순수 분말 유동
- Zn·Na·K 이온, 슈퍼커패시터, 연료전지
- ⚠ **DEM/FEM 을 서로 캘리브레이션한 논문은 무관이 아니라 반례**다 — 관련도는 높게 주되
  frame[4] 위반으로 **비판 포인트**에 반드시 적는다

## 축 B (DFT / MLIP) — 브랜치 `claude/friendly-meitner-lldvar`

**한 줄**: 황화물 SE(Li₆PS₅Cl 계열)의 전자구조·탄성·결합·이온수송을 제일원리와 MLIP-MD 로
정량하고, LiNiO₂ 계면 위 **바인더 조각의 흡착 대비**와 SEI 분해상의 **Li 이동 장벽**을 낸다.
그런데 이 축의 정체성은 물리보다 **절차**에 있다 — 계산 전에 보고량을 정의하고, 사전등록하고,
게이트를 결과 보기 전에 박고, 못 확인한 것을 통과로 세지 않는다.

> ⛔ **이 축의 통제 규율 (2026-08-28 채택)** — *"admissible state 가 여럿인데 선택·집계 규칙이
> 없으면 스칼라 보고량은 정의되지 않는다."* 열린 껍질 · 자성 기판 · 산화환원 활성이 그 위험
> 신호다. 채택 배경이 그대로 이 축의 성격을 말한다: **SDCP 흡착에너지를 여덟 번 계산했고 여덟 번
> 반려됐다.** 받은 리뷰는 전부 *"제대로 돌렸나"*(무결성·해시·INCAR·게이트)였고 전부 통과했다.
> *"맞는 양을 재고 있나"* 는 여덟 번째에야 물었고 즉시 P0 가 나왔다.
> ⇒ 문헌을 읽을 때도 **"이 논문은 무엇을 보고량으로 정의했는가, 상태 선택 규칙이 있는가"**
> 가 비판 포인트의 1순위다.

### 쓰는 도구·코드 (repo 경로 · 크기순)
- `tools/sdcp/vasp_handoff_bundle.py` (**1.37 MB · ~21k줄**) — 이 축에서 제일 큰 물건.
  VASP 외주 **번들 생성기 + 배포 분석기(`analyze_results.py` 템플릿) + 단계 러너
  (`run_staged.sh`) + POTCAR 루트 봉인(`SEAL_POTCAR_ROOT.sh`) + census** 가 한 파일에 있다.
  `--selftest` 437건 · verify 30 · e2e 15 (stub VASP 로 census→봉인→1단계 관통)
- `tools/sdcp/build_v7c_trimer.py` (581 KB) — SDCP 올리고머 빌더 (ORCA 계열)
- `tools/sdcp/site_screen.py` (178 KB) · `run_orca_stage_a.sh` — 자세·자리 스크리닝, ORCA r2SCAN-3c Opt
- `tools/sdcp/vasp_cost_estimate.py` — 비용·makespan 모형 (2026-09-04 단계 게이트·KPAR 반영)
- `tools/sei/symmetric_saddle.py` (175 KB) · `build_neb_inputs.py` (89 KB) · `collect_neb.py` — QE CI-NEB
- `tools/ionic/msd_diffusive_check.py` (138 KB) · `tools/modelc_v3/` — UMA MLIP-MD, MSD·아레니우스
- `tools/cascade/build_screening_funnel.py` (94 KB) — 도핑·산화안정성 스크리닝 깔때기
- `tools/comp1_v3/` — BVSE (softBV) · `tools/electronic/` (37) — fixed-occ nscf 갭·DOS·LOBSTER
- `tools/oxidation/` (45) · `tools/doping/` (56) · `tools/neb_diffusion/` (32) · `tools/vgcf_hbn/` (19)
- `tools/litdb/extract_figures.py` (88 KB) — 논문 그림 크로핑 · `tools/figures/` (84) — 하우스 스타일
- `tools/kb_wiki.py` — kb 위키 index/lint · `tools/convention_check.py` — 물리 규약 복사본 갈림 감시
- `webapp/` — `canonical.py` 가 `canonical_registry.json` 의 `source_path`+`source_key` 를 따라가
  원자료와 **대조**한다 (`tools/db/validate_canonical.py`)

### 캠페인 — 이게 실제 목록이다 (11개)

`db/properties/` **407 파일** · `kb/` **351 문서** 전수조사(2026-09-04) 결과. 축 B 는 한 개
과제가 아니라 **열한 개 캠페인**이고, 논문 관련도는 *"어느 캠페인에 붙는가"* 로 판정한다.

**① LPSCl 계열 벌크 물성** (`b2o3` 36 · `lpsocl` 30 · `comp2` 10 · `modelc` 7 파일)
comp1–comp5 · `modelc`(=LPSCl1.6) · **+B₂O₃** · **LPSOCl**(O 치환) · **Nd 치환**.
밴드갭(fixed-occ nscf) · B₀(BM3 EOS) · 탄성(relaxed-ion) · **ICOHP**(LOBSTER) ·
Bader/Löwdin 전하 · ELF 공유성 · phonon 안정성 · Voronoi 무질서 · convex hull · γ_SE.
→ 값은 아래 표. 관련 논문: 황화물 SE 의 전자구조·기계물성·결합해석.

**② 이온수송 MLIP-MD** (`msd` 9 · `md` 5 · `uma` 18 · `vanhove` 2 · `beta` 3 파일)
UMA-s-1p1(omat) Langevin NVT. D₀ 분해 · Van Hove 고원 · β-gate · dualx blocking.
→ Ea 멀티시드 **0.197 eV**. 관련 논문: MLIP(MACE/CHGNet/M3GNet/UMA) MD 로 σ·Ea 를 낸 것,
그리고 **AIMD vs MLIP 대조**를 한 것(우리가 UMA 3.3배 과소를 실측했으므로 특히 값어치 있다).

**③ BVSE 이온 경로** (`bvse` 9 · `bv` 5 파일) — softBV. B₂O₃ 채널 **3.32 / 4.74 / 6.73 %**.
관련 논문: bond-valence 경로 해석, 그리고 BVSE 를 NEB 대용으로 **절대값 인용**한 논문(비판 대상).

**④ 산화안정성 cascade** (`cascade` 53 · `oxidation` 8 파일) — MP grand-potential ESW.
**host Li₆PS₅Cl: 환원한계 1.242 V · 산화한계 2.14 V · OCV 자가분해 1.717 V · 창 0.898 V**,
산화 onset 반응 `4 Li₆PS₅Cl → LiS₄ + 4 Li₃PS₄ + 4 LiCl + 7 Li`. 지금 method-comparable 270건.
★ **`phase_set_id` 계약** = sha256(정렬된 MP entry_ids)[:16] — **같은 phase_set 안에서만**
후보↔host 비교가 성립한다. ⇒ 문헌의 ESW 값은 **어느 상집합·어느 MP 스냅샷**인지 없으면
우리 창(0.898 V)과 나란히 못 쓴다. 그 확인이 이 캠페인의 비판 포인트 1순위.

**⑤ 도핑 스크리닝 깔때기** (`doping` 3 · `site` 2 · `codoping_ml` 2 파일)
**큐레이션 89종** 도펀트를 Xiao 2019 F1–F6 · Sendek 2017 · Kahle 2020 표준 게이트로 재표현.
waterfall **89 → 89 → 84 → 45 → 28 → 1** (G1 구조안정 → G2 전기화학창 → G3 산화 onset →
G4 Li 수송 → G5 기계). ⛔ 파일이 스스로 적고 있다: *"게이트 통과 수는 **발견 성능 지표가
아니다**"* · `_v2` 는 **미검증 진단물**(G3 phase_set_id 미기록 · G4 blocking 이 BVS 를 덮는
순환 · G5 로스터 상대 median). **순위·통과 수를 결과로 인용 금지.**
⇒ 문헌의 high-throughput 스크리닝 논문은 여기 직결이고, *"통과 수를 성능으로 보고했는가"*
가 곧 비판 포인트다.

**⑥ SEI 분해상** (`sei` 14 · `neb` 13 파일) — Li metal(bcc) · Li₂S · Li₃N–Nd · Li₂O · Li₃P ·
Li₃PO₄(β/γ) · LiCl · LiNdO₂ · Nd₂O₃ · Nd₂S₃ 의 밴드갭(fixed-occ) + MP 형성전위 +
**QE CI-NEB Li 이동장벽**. 값은 아래 표(전건 `citable=false`).

**⑦ SDCP–PTFE 바인더 계면** (`sdcp` 27 파일 + `runs/sdcp_*` 5개) — **이 축의 주력**.
LiNiO₂(104) 슬랩 192원자 × 바인더 조각, **SDCP(설폰화 전도성 고분자) vs PTFE(C10)**,
자기 seed 2종 `afm2424_pm1` / `afm2424_net4` · U(Ni d)=6.2 · D3 zero-damping.
→ **C-12 외주 VASP 16잡(ΔE_ads)은 아직 값 없음, 발송 전.**
+ SDCP polaron Stage A(ORCA r2SCAN-3c, gs0–gs2 완료 각 10–18 h) · site_screen · v7c trimer 빌더.

**⑧ AF-ASSB 음극 계면 — Li₃N(001) / LiC₆(0001)** (`li3n` 9 파일)
Li adatom 확산장벽을 **UMA · DFT-SCF · 전 DFT NEB 3중**으로 대조:
Li₃N(001) path A **UMA 0.054 → DFT SCF 0.0486 → 전 DFT CI-NEB 0.18 eV** ·
LiC₆(0001) DFT SCF **0.309 eV**. ⇒ **UMA 가 3.3배 과소**였다는 것이 이 캠페인의 소득이고,
CLAUDE.md 의 *"UMA 를 Li₃N 에 사용 금지"* 가 여기서 나왔다.
**AgNO₃–C–PVP 원고(v5) SI Table S2** 가 이 파라미터표다.

**⑨ VGCF / h-BN 갤러리** (`vgcf` 7 파일) — 탄소섬유 위 h-BN 층간 Li 이동.
QE neb.x 7 images · CI auto · PBE-D3BJ · 4×4 · k 3×3×1. 결합 2×2 매트릭스
(gallery_2L1L **−1.580** · gallery_1L2L **−1.592 eV**). h-BN 단층 위 표면확산 **Ea 0.007 eV**
= 수치 분해능 이하 ⇒ *"< 0.01 eV, 사실상 무장벽"* 으로만 보고하고 **Shi 2017 의 0.10 eV 와
일치한다고 쓰지 않는다**(13배 낮다). ★ **층 민감도 −209.4 meV vs E_bind 산포 52 meV**
⇒ *"장벽은 같은 host 위 site 에너지 차라 층 효과가 상쇄된다"* 는 가정을 **반증**했다.

**⑩ 계면 분해 per-seed** (`interface` 12 파일) — b2o3 / modelc2x / modelc62 / **lpsocl** ×
seed 2·3·4 (각 500행 CSV). 전압분해 계면 반응성을 시드별로 남긴다(평균만 남기지 않는다).

**⑪ Zn ALZIB (C1, 수계)** (`zn` 2 파일) — Cu–Zn 상 지문. **43°±1° 안에 8상이 1.47° 폭으로
겹치고 Cu–Zn 간격은 0.097°** ⇒ 회절 기하가 강제하는 것이라 분해능으로 못 푼다.
DFT 격자상수로 가르려는 시도는 **틀렸다**(DFT 오차 ~1 % = 2θ 0.3–0.4° ≫ 0.097°).
⇒ DFT 가 기여할 자리는 **convex hull 하나** — 어느 상을 후보에서 뺄 수 있는가.
⚠ **수계 Zn 계다. 황화물 SE 수치와 같은 표에 놓지 않는다.**

### 관심 물리량과 현재 확보된 값
`db/properties/canonical_registry.json` — 정본 **39항목**. 각 항목이 `source_path`+`source_key` 로
원자료를 가리키고 `resolve()` 가 따라가 대조한다. **스크립트에 흩어져 있지 않다.**
`comparison_group` 이 같은 값끼리만 순위·비교·레이더에 올린다.

| 물리량 | 값 / 범위 | 상태 |
|---|---|---|
| Band gap (fixed-occ nscf 고유값) | comp1 **2.066** · modelc **2.099** · +B₂O₃ **1.9671** · LPSOCl **2.2309** eV | canonical |
| B₀ (BM3 EOS) | 21.71 – 26.233 GPa | canonical |
| 탄성 (relaxed-ion) | 20.03 – 35.04 GPa (E_VRH 22.06 / 27.66) | canonical |
| MD 활성화에너지 (멀티시드) | 0.197 eV | canonical |
| MD 활성화에너지 (단일시드 앵커) | 0.1512 – 0.2867 eV | provisional |
| ICOHP (LOBSTER 결합당) | −5.913 – −6.04 eV | canonical |
| SDCP wave1 ΔE(site) | 9.265 · 36.071 · 36.157 · 49.767 meV | canonical |
| SDCP wave1 E_ads (box24) | −0.3302 – −0.7728 eV | provisional |
| NEB Li 이동장벽 (SEI 상, QE) | Li metal **0.0806** · LiNdO₂ **0.229** · Li₂S **0.305** eV | **전부 `provisional_single_cell` · citable=false** (최상위 `retracted: true` = n_citable 0) |
| 표면에너지 γ_SE | 0.45 – 1.211 J/m² | — |
| **전기화학 창 (host Li₆PS₅Cl, MP grand-potential)** | 환원 **1.242** · 산화 **2.14** · OCV 자가분해 **1.717** V → 창 **0.898 V** | `phase_set_id` 결박, 같은 상집합 안에서만 비교 |
| BVSE 채널 분율 (B₂O₃) | **3.32 / 4.74 / 6.73 %** | 원본 주기셀 값만 (큐빅 박스는 표시용) |
| Li₃N(001) Li adatom 장벽 (path A) | UMA **0.054** → DFT SCF **0.0486** → **전 DFT CI-NEB 0.18 eV** | UMA 3.3배 과소 ⇒ Li₃N 에 UMA 금지 근거 |
| LiC₆(0001) Li adatom 장벽 | DFT SCF **0.309 eV** | AF-ASSB SI Table S2 |
| h-BN 위 Li 표면확산 | **0.007 eV** (= 수치 분해능 이하) | *"< 0.01 eV, 사실상 무장벽"* 으로만 서술. Shi 2017 0.10 eV 와 일치 주장 금지 |
| h-BN 갤러리 결합에너지 | 2L1L **−1.580** · 1L2L **−1.592 eV** (층 민감도 **−209.4 meV** vs E_bind 산포 52 meV) | "층 효과 상쇄" 가정을 **반증**함 |
| 도핑 깔때기 통과 수 | 89 → 89 → 84 → 45 → 28 → 1 | ⛔ **결과로 인용 금지** — `_v2` 는 미검증 진단물 |
| Cu–Zn 상 지문 (Zn ALZIB) | 43°±1° 안 **8상 / 1.47° 폭**, Cu–Zn 간격 **0.097°** | 수계 Zn 계 — 황화물 SE 와 같은 표 금지 |
| **C-12 ΔE_ads (SDCP vs PTFE)** | **아직 없음 — 외주 VASP 16잡 발송 전** | 미계산 |

### 방법론적 쟁점 (= 데이터 규율. 어기면 값이 무효다)
- **Band gap 은 fixed-occupations nscf 의 VBM/CBM 고유값만 인정.** DOS-threshold 판독 금지
  (~0.3 eV 과소). 정본 registry 에 `prohibitions: [dos_threshold_readout]` 로 **기계 집행**된다.
- **UMA 를 Li₃N 에 사용 금지** (2026-06 결정론적 편향 판정). LPSCl 계열 MD 에는 검증된 표준.
- MLIP-MD: **MSD 창 2–50 ps 고정** · 아레니우스 600/800/1000 K 3점(400/500 K 제외) ·
  Nernst–Einstein(Haven=1) · **σ 절대값 인용 금지, 비율도 멀티시드 판정만**
  (단일시드 1.33× 철회 사례). Ea 오차막대는 600 K 3-시드.
- **BVSE 정량·순위는 원본 주기셀 값만** (큐빅 박스는 표시용, ±1.3 %p 표본 편차).
  softBV R₀ = S 2.105 / Cl 2.249 / O 1.466, b=0.37 · ~0.25 Å voxel
- **NEB 전하 규약이 상의 `electronic_class` 로 갈린다** — 부도체 = V_Li⁻(tot_charge −1) + jellium
  + gaussian smearing / 금속 = 중성 공공(tot_charge 0) + mv smearing. jellium 은 유한셀 근사라
  **셀 수렴 확인 전에는 상 사이 비교 전용.** ⛔ BVSE 프록시와 같은 표 금지(단위는 같아도 다른 양).
- **POTCAR 신원**: `post_hoc` 정책 ⇒ 이 묶음 결과는 **원고 인용 자격이 없다**(탐색용).
  사후 attestation 으로 승격 불가 — 계산 **전** 외부 앵커(사전 승인 해시 또는 서명)여야 한다.
- **상태 선택 정책** — "전 계에 같은 NUPDOWN 값" 이 아니라 같은 *state-selection policy* 다.
  실측 사고: 기체 기준은 `NUPDOWN=0` 으로 **제약**됐는데 복합체는 `−1` 자유라
  **제약된 기준에서 자유로운 복합체를 뺐다.**
- **평균류 지표는 그림 표시 창과 동일한 창**(−8..0 eV)으로 계산·인용.
- 슬랩은 기하 승계(verified-carry: 마지막 ATOMIC_POSITIONS 스플라이스 + 검증) + local-TF/저β 믹싱.

### 거버넌스 기계 (이 축의 진짜 산출물)
- `db/governance/decisions.json` — 결정 **14건**. `proposed → (사람 ratify) → active` 이고
  ratification 은 `content_digest`(비준 대상 내용의 sha256)로 결박된다. 내용을 고치면 지문이
  어긋나 **재승인을 요구**한다. 주요 결정: `estimand-before-compute` · `closure-criteria-first` ·
  `missing-axis-is-unknown-not-worst` · `source-authority` · `hash-bound-carry` · `no-fallback` ·
  `sdcp-c12-path`(active) · polaron F_bb / S0 4층 게이트(proposed)
- `db/properties/*_prereg_*.json` — 사전등록. C-12 는 `3_오차예산` 에 B_num = |Δ_vac|+|δ_gas|+|δ_k|,
  문턱 5 meV, **"축이 하나라도 없으면 NUMERIC_BUDGET_INCOMPLETE — 확인 못 한 것은 통과가 아니다"**
- **마감 규율**: `db/properties/<계>_closed_<날짜>.json` 에 확정값·허용 서술·**금지 서술**·재개 조건.
  순서가 핵심 — 데이터를 보고 닫지 않고, 조건을 먼저 정하고 그게 채워졌으므로 닫는다.
  선례 `sdcp_neutral_closed_2026_08_28.json` (SDCP 는 조건 없이 두 번 닫았다가 두 번 물렸다)
- **인용자격 계약** (`citability_contract_2026_08_16`) — 셀 수렴 미시험이면 자동으로
  `provisional_single_cell` · `citable=false` 로 강등. `sei_neb.json` 은 인용가능 0/9 이라
  최상위 `retracted: true`
- `kb/` **관리 문서 351개** — `reviews`(106) · `results`(94) · `methodology`(49) · `seminars`(38) ·
  `projects`(23) · `papers`(20) · `elements`(118) · `questions`(10) · `syntheses`(6).
  frontmatter 필수 · `explored` 는 **사람만** true · 근거 하나면 `confidence: high` 금지 ·
  `kb_wiki.py lint` 0 errors 유지
- **외부 감사 사슬** — Codex/외부 리뷰어 회신을 `kb/reviews/` 에 원문 보존하고 회신 ID(AI·AO·AR·
  AT·AV·AZ·BA·BB·BD·BE·BF·BG·BH …)로 코드 주석에 결박한다. 코드에 *"⛔ 회신 BH P0-1"* 처럼
  **어느 리뷰가 어느 줄을 낳았는지**가 적혀 있다.

### 진행 중 / 끝난 것
- **진행**: **C-12 외주 VASP 번들** — v31→v34 반복, 내부 6렌즈 리뷰가 v34 **NO-GO**
  (P0: 선택 attestation 이 실물에서 1단계 게이트를 막는다 / δ_k 축 설계 제외가 비준 사전등록과 어긋난다).
  v35 준비 중이고 **δ_k 재개 조건 1저자 결정이 유일한 블로커**.
  · SDCP polaron Stage A (ORCA r2SCAN-3c, gs0–gs2 완료 각 10–18 h, gs3–gs6 대기)
  · SEI NEB 다중 기계 병합 (li_metal CI-NEB 완료) · Cu–Zn convex hull 보고량 카드(계산 전)
  · Nd 치환 조사 · 산화안정성 cascade
- **끝**: LPSCl 밴드갭·탄성·ICOHP 정본화 · `sdcp_neutral_closed_2026_08_28` · AF-ASSB SI v6 제출본
- **자원**: KISTI neuron(Slurm) · kgy RTX3090(QE-GPU + uma) · gabia A6000(pw.x/UMA **동시 실행 금지**)
  · desktop WSL(ORCA) · **외주 VASP**(슈퍼컴 sbatch, 잡당 walltime 상한 91 h)

### 이 축과 무관한 논문의 특징 (오탐 감축용)
- 입자 패킹·압축·DEM·미세구조 유한요소 — **그건 축 A 다**
- 셀 조립·캘린더링·건식전극 공정 최적화, 파일럿 스케일업
- 계산이 전혀 없는 순수 실험 (합성 + cycling curve 만) — **단, EIS·대칭셀은 축 C 다**
- 액체·폴리머 전해질 전용 · Li–S(황화물 SE 아님) · Na/K 이온
  ⚠ **Zn 은 예외다** — 캠페인 ⑪(Zn ALZIB, 수계)이 살아 있다. **Cu–Zn 상동정·XRD 상지문·
  convex hull** 이면 관련(0.5–0.7), 그 밖의 수계 Zn 전기화학은 무관(< 0.35).
  단, 관련이어도 **황화물 SE 수치와 같은 표에 놓지 않는다**
- 머신러닝이되 **원자 스케일 퍼텐셜이 아닌** 것 (제조 파라미터 회귀, 이미지 분할 only)
- DFT 이되 배터리와 무관한 계 (촉매 · 태양전지 · 열전 · 수소저장)
- ⚠ **DOS threshold 로 밴드갭을 읽은 논문**, **단일 시드 MD 로 σ 비를 주장한 논문**,
  **NEB 를 셀 수렴 없이 절대값으로 인용한 논문** 은 무관이 아니라 **비판 대상**이다 —
  우리가 그 함정을 각각 규율로 닫았기 때문에 세미나 질문·리뷰어 관점에서 값어치가 크다

## 그 외 축

### 축 C — 실험 협업 (`이종기술`, 한양대 이종원 그룹) ★ 별도 축이다
축 A 브랜치의 `이종기술/` 은 폴더가 아니라 **독립 실험 라인**이다 (README 첫 줄:
*"Separate experimental line from SDCP"*).
- **계**: 소립(4 µm single-crystal) NCM 양극 No.1 / No.2 + poly:small **5:5** bimodal 블렌드,
  **SUS** 집전체. 조성 AM:SE:VGCF:PTFE = **80:18:1:1**.
  공정: vortex 10 min → PTFE → ball-mill 1 h → Thinky 2000 rpm 5 min → hot-plate rolling → roll-press
- **셀**: 대칭셀 SUS∣복합양극∣SUS (이온 차단 → σ_e) · 풀셀 SUS∣Li-In∣SE-bulk∣복합양극∣primer-SUS
  · 대칭 ⌀10 mm(0.785 cm²) · 율특/수명 ⌀13 mm(1.327 cm²)
- **측정**: BioLogic **VSP-300** (EC-Lab v11.63) EIS — `이종기술/eis/raw/*.mpr` 원자료 +
  `extracted/*.csv` (freq_Hz, ReZ_ohm, negImZ_ohm, absZ_ohm, phase_deg, Ewe_V, I_mA, cycle)
  + `eis_catalog.csv` + `fits/` (CNLS 등가회로 R_s / R_int / R_w / R_ion). 도구 `scripts/eis_archive.py`
- **확보된 값**: 비용량(5:5) No.1 **202.95** · No.2 **206.5** mAh g⁻¹ · 면적용량 목표 3 mAh cm⁻² ·
  Li-In 음극 · 60 °C · 0.1C 2사이클 → 0.2C
- **어떻게 축 A 로 들어가나**: 풀셀 EIS → **R_int** 가 STEP4 의 실측 앵커 (V_term = V − I·R_int).
  ⚠ 이건 SDCP 원고의 SBE/DBE 패널 값과 **다른, 이 프로젝트 자신의 측정값**이다.
- ⇒ **실험 논문(EIS·대칭셀·율특성·Li-In·SUS 집전체)은 무관이 아니다.** 축 C 로 채점한다.

### 그 밖
- **세미나·발표**: `kb/seminars/` · `kb/papers/lpscl_vs_lpscl16_seminar_v1.pptx` ·
  `litdb/papers/*__seminar_5min_qa.md` (5분 Q&A 형식 digest 3건) — 축 B 의 전달 형태.
- **AF-ASSB 원고 협업**: `docs/collab/` · AgNO₃–C–PVP 원고 SI 기여 (축 B). 계산이 실험 원고 SI 를 받친다.
- **웹앱**: 양 브랜치 모두 Flask 웹앱 (축 A 케이스 브라우저 + 3D 뷰어 / 축 B 정본값 뷰어).
- **거버넌스가 그 자체로 산출물이다** — 축 A `docs/reviews/claims.json` (주장 82건: live 53 ·
  rejected 20 · hold 5 · retired 4 + `quotation_ban` 인용금지 목록) · `findings.json` (결함 123건:
  claimed_fixed 93 · open 19 · verified 8 · wontfix 3, `check_review_findings.py` 가 자기일관 강제) ·
  `wiki/` 21페이지 · 사전등록 `docs/reviews/*_prereg_*.md`.
  축 B `db/governance/decisions.json` · `db/properties/*_prereg_*.json` · `kb/` 351문서.
  ⇒ **양쪽 다 "결과를 보기 전에 게이트를 박고, 틀린 것을 원장에 남긴다."** 이것이 두 축의
  진짜 공통점이고, 논문을 읽을 때 **비판 포인트를 잡는 기준**이다.

---

## 논문 원고 현황

| 축 | 경로 | 제목 / 무엇 | 진행 | 타깃 저널 |
|---|---|---|---|---|
| A | `docs/paper/main.tex` + `refs.bib` (브랜치 stoic-knuth) | *Stage E fracture-aware network solver for all-solid-state battery cathode microstructure: a literature-grounded multi-physics framework with 7-layer defence and Bruggeman fallback* (저자 필드 `Yonghoon Kim`, KAIST — ⚠ 이름 표기 확인 필요) | 본문 1034행+, 전 섹션 초안. 공저자 편집 시트 진행 중 (`docs/reviews/` 최근 30일 477파일) | **unknown** |
| A | `docs/manuscript_sdcp_sigma_e_mechanism.md` (최종판) + `docs/sdcp_318_base_sbe_dbe_comparison.md`(수치 원장) | SDCP σ_e 기전 원고 | ⚠ **2026-08-13 부로 헤드라인 철회** (격자 미수렴). 잔여 = **E_bind DFT** | unknown |
| A | `docs/manuscript/Methods_simulation_v7_for_coauthors.docx` · `docs/manuscript_draft/DEM_methodology_and_tables_v1.docx` | 공저자용 시뮬레이션 Methods | 정본 rev7 | unknown |
| B | `docs/manuscripts/Methods_DFT_v9_for_coauthors.docx` · `Methods_simulation_v8_for_coauthors.docx` · `Table_S2_DFT_parameters.docx` · `Figure2e_explained_v10.docx` | **AF-ASSB AgNO₃–C–PVP 원고(v5)** 의 Methods·SI (Table S2 = Li₃N(001)/LiC₆(0001) DFT 파라미터) | SI v6 제출본 형태 확정(`--nonotes`). 각주 3항목은 리비전에도 안 넣기로 확정 | unknown |
| B | `kb/papers/draft_v1.md` · `computational_methods_draft.md` · `final_report_v2.md` | 내부 초안 | unknown | unknown |

**`use_in_my_paper` 를 쓰는 법** — 축마다 지목 단위가 다르다:
- 축 A: `main.tex` 의 **절 이름으로** 지목할 수 있다. 실제 절 —
  Introduction / Methodology (DEM particle configuration · Contact-network extraction and Kirchhoff
  solve · Three parallel transport channels) / Stage E literature-grounded grain corrections /
  7-Layer defence and Bruggeman fallback / Results (Pipeline self-consistency · Trust audit ·
  Variance decomposition · Cell-level ASR validation · Design rule AM_P fraction vs σ_e loss ·
  Strict physics-first porosity prediction) / Discussion (Two competing densification mechanisms ·
  Why we do not fit out-of-regime deviations · Limitations · Hooke–Hertz equivalence ·
  SE–SE grain boundary · Bruggeman upper bound · Porosity wave-shape sensitivity ·
  Stress-bearing percolation) / Conclusion
  → 예: *"§6.6 SE–SE grain-boundary 문단에 인용"*
- 축 B: 원고가 .docx 라 절 지목이 어렵다. **`kb/` 카드나 `db/properties/` 항목으로** 지목하는 편이
  정확하다 → 예: *"`kb/methodology/` 의 NEB 셀 수렴 카드에 반례로 인용"*
- 축 C: 아직 원고가 없다. **앵커 대기 큐**(`[[anchor-waitlist]]`)의 어느 항목을 채우는지로 지목한다.

## 관련도 채점 가이드 (구조는 고정, 기준선은 브랜치가 조정)
| 점수 | 기준 |
|---|---|
| 0.9–1.0 | 두 축 중 하나의 **내 시스템·내 방법**에 직접 해당. 수치·방법을 바로 비교·인용 가능 |
| 0.7–0.85 | 같은 방법이되 시스템이 다르거나, 같은 시스템이되 방법이 다름 — 파라미터·검증 데이터로 활용 |
| 0.5–0.65 | 황화물 ASSB 일반(계면·전해질·공정) 실험·리뷰. 배경·도입부 인용용 |
| 0.35–0.45 | 배터리이나 두 축 어느 쪽과도 연결이 약함 |
| < 0.35 | 무관 — rejected (DB에는 기록) |

> 한 논문이 두 축을 모두 만족할 필요는 없다. **한 축만 맞아도 높은 점수**를 준다.
> 반대로 두 축을 억지로 잇는 서술을 만들어 점수를 올리지 않는다.

**브랜치가 조정한 기준선 (2026-09-04)**
- 0.9 이상을 주려면 다음 중 하나가 있어야 한다: ① LIGGGHTS/DEM 으로 만든 복합양극 미세구조에서
  **수송 물성(σ, τ, percolation)** 을 뽑았다 ② 저항망/Kirchhoff/Bruggeman 으로 ASSB 양극을 풀었다
  ③ Li₆PS₅Cl 계열의 **밴드갭·탄성·ICOHP·MLIP 확산**을 계산했다 ④ LiNiO₂/NCM 계면 위 **바인더·분자
  흡착**을 DFT 로 쟀다 ⑤ SEI 상(Li₂S·Li₃N·Li₂O·Li₃P·LiCl)의 **Li 이동 장벽**을 NEB 로 냈다
- **Cronau · Trevisanello · Wang · Lawn · Auerbach · Holm · Duquesnoy · Bielefeld · Ngandjong**
  을 인용하거나 그 값을 쓰는 논문은 축 A 에서 0.8 이상으로 본다 (Stage E 보정의 출처들이다).
- 실험 논문이라도 **입경 분포 + 압축압력 + porosity/ASR 를 함께 보고**하면 축 A 0.7 이상
  (우리 검증 데이터가 된다).
- 실험 논문이라도 **σ_ionic 의 온도의존성 + 활성화에너지**를 보고하면 축 B 0.7 이상.

## 채점용 용어 가중치 (규칙 기반 fallback — `research_agent/triage.py` 와 함께 유지)
- **축 A 핵심**: `discrete element`, `DEM`, `LIGGGHTS`, `MPM`, `material point method`, `Taichi`,
  `voxel`, `resistor network`, `percolation`, `Kirchhoff`, `Bruggeman`, `constriction resistance`,
  `effective medium`, `tortuosity`, `Heckel`, `coordination number`, `force chain`, `Auerbach`,
  `cold press`, `uniaxial compaction`, `dry electrode`
- **축 B 핵심**: `first-principles`, `DFT`, `density functional`, `ab initio`,
  `machine learning potential`, `MLIP`, `AIMD`, `NEB`, `nudged elastic band`, `COHP`, `ICOHP`,
  `LOBSTER`, `bond valence`, `BVSE`, `band gap`, `VASP`, `Quantum ESPRESSO`, `PAW`, `DFT+U`,
  `formation energy`, `convex hull`, `electrochemical stability window`
- **축 B 캠페인별 보강** (전수조사 2026-09-04 — 위 목록만으로는 ④⑤⑧⑨⑪ 이 안 잡혔다)
  · ②MLIP-MD: `MACE`, `CHGNet`, `M3GNet`, `universal interatomic potential`,
    `foundation model potential`, `Nernst-Einstein`, `mean squared displacement`, `Arrhenius`,
    `Haven ratio`, `Van Hove`
  · ④산화안정성: `grand potential`, `grand canonical`, `Materials Project`, `decomposition energy`,
    `decomposition reaction`, `pseudo-binary`, `mutual reaction energy`, `oxidation limit`,
    `reduction limit`
  · ⑤도핑: `dopant`, `doping strategy`, `high-throughput screening`, `substitutional`,
    `aliovalent`, `descriptor`, `screening funnel`
  · ⑦바인더 계면: `adsorption energy`, `binding energy`, `slab`, `surface energy`, `polaron`,
    `sulfonated`, `conducting polymer`, `LiNiO2`, `van der Waals correction`, `D3`
  · ⑧음극 계면: `Li3N`, `lithium nitride`, `LiC6`, `graphite intercalation`, `adatom`,
    `surface diffusion`, `migration barrier`
    (⚠ `anode-free`/`anode-less` 는 `triage.py` 에 **이미 core 로 들어 있고 그대로 둔다** —
     캠페인 ⑧ 이 살아 있기 때문이다. 사용자가 2026-09-04 중단시킨 것은 **Scholar alert
     검색어 등록**(수집)이지 채점이 아니다. ⛔ alert 를 다시 등록하지 말 것)
  · ⑨VGCF/h-BN: `hexagonal boron nitride`, `h-BN`, `gallery`, `interlayer`, `carbon fiber`
  · ⑪Zn ALZIB: `Cu-Zn`, `brass`, `phase identification`, `Rietveld`, `XRD pattern`
    (⚠ 이 다섯만 Zn 감점을 상쇄한다. 일반 `zinc-ion` 은 감점 유지)
- **축 C 핵심** (실험 협업): `impedance`, `EIS`, `symmetric cell`, `blocking electrode`,
  `Li-In`, `areal capacity`, `single crystal NCM`, `polycrystalline NCM`, `rate capability`,
  `stack pressure`, `roll press`, `equivalent circuit`, `R_int`, `charge transfer resistance`
- **공통 시스템**: `all-solid-state`, `sulfide`, `Li6PS5Cl`, `LPSCl`, `argyrodite`,
  `halide electrolyte`, `composite cathode`, `NCM811`, `NMC811`, `NCM83`
- **물성·공정**: `porosity`, `tortuosity`, `compaction`, `calendering`, `contact`, `elastic`,
  `modulus`, `adhesion`, `interface`, `NCM`, `ASR`, `area specific resistance`,
  `binder`, `PTFE`, `PVDF`, `VGCF`, `carbon additive`, `conductive additive`
- **감점**: `supercapacitor`, `zinc-ion`, `sodium-ion`, `fuel cell`, `photocatal`,
  `perovskite solar`, `redox flow`, `thermoelectric`, `hydrogen storage`, `CALPHAD`,
  `battery management`, `state of charge estimation`, `pack thermal management`
- 프리프린트(arXiv 등)는 IF 0 — relevance만으로 tier 결정
- ⚠ `\bNCM\b` 만 쓰면 `NCM811` 이 단어경계에서 안 잡힌다 — 두 형태를 다 넣을 것

## 심층 분석 시 반드시 채울 항목 (형식은 고정)
1. 비교 가능한 **수치** — 단위와 조건 포함
2. **방법론 세부** — 해당 축의 계산 조건
   (축 A: 접촉 모델·강성·마찰·압축압력·입경분포·셀 크기 / 축 B: functional·k-point·supercell·U 값·
   MLIP 학습 데이터·앙상블·MSD 창)
3. **내 결과와의 일치/충돌** — 위 "확보된 값" 표와 대조. ⚠ 축 B 의 NEB·E_ads 는 아직
   `provisional` 이므로 "우리 값과 일치" 라고 쓰지 말고 "우리 잠정값과 같은 자릿수" 로 쓴다
4. **인용 포인트** — 축 A 는 `main.tex` 절 이름, 축 B 는 `kb/` 카드 또는 `db/properties/` 항목
5. **비판 포인트** — 세미나 질문·리뷰어 관점

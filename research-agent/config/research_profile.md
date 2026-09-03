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
> (`git merge-base` rc=1). 코드도 공유하지 않는다. 다만 **딱 한 군데 접점**이 있다: 두 브랜치가 각각
> 공저자용 Methods 문서를 낸다 (축 A `docs/manuscript/Methods_simulation_v7_for_coauthors.docx`,
> 축 B `docs/manuscripts/Methods_simulation_v8_for_coauthors.docx`). 같은 계보의 문서로 보이나
> **같은 원고인지는 확인하지 못했다 (unknown)** — 파일이 .docx 라 본문 대조를 안 했다.
> 이것은 "파이프라인" 이 아니라 **같은 학회/원고에 각자 Methods 를 기여**하는 관계다.

---

## 축 A (DEM / MPM / voxelization) — 브랜치 `claude/stoic-knuth-NObVQ`

**한 줄**: LIGGGHTS 로 황화물 복합양극을 준정적 압축해 만든 입자 패킹에서 접촉망을 뽑아,
Kirchhoff 저항망으로 이온·전자·열 세 채널을 풀고, 파괴(Lawn/Auerbach)와 문헌 기반 grain 보정을
접촉마다 걸어 ASR 까지 가는 파이프라인.

### 쓰는 도구·코드 (repo 경로)
- `dem_scripts/*.liggghts` — LIGGGHTS 준정적 압축 입력. `dem_scripts/oat_sweep/` (OAT 감도 스윕)
- `scripts/network_conductivity.py` — 접촉망 → Kirchhoff 풀이 (σ_ionic, σ_e, κ)
- `scripts/run_network_full_corrections.py` — **Stage E** (Lawn 파괴 × grain 보정), Bruggeman fallback
- `scripts/find_and_rerun_stage_e.py`, `backfill_validation_flags.py`, `audit_validation_flags.py`
- `scripts/pca_ensemble_variance.py` — 분산 분해 + PCA biplot
- `scripts/plot_porosity_4panel.py` — porosity 검증 4패널
- `webapp/app.py` — Flask 케이스 브라우저 + 3D 뷰어
- `heckel/` (Heckel 압축 해석), `se_curve/`, `machine-learning/`, `pipeline/`, `이종기술/eis/`
- `skills/dem-analysis-standard.md`, `skills/dem-analysis-bimodal.md`
- ⚠ **MPM / voxelization 은 이 브랜치에서 1급 코드로 확인되지 않았다.** `docs/codex_dem_mpm_response_20260811.md`
  같은 리뷰 응답 문서와 litdb digest(`devaucorbeil2020_mpm_after_25_years_review.md`,
  duquesnoy2020 calendering **voxel** 생성기)로만 나타난다 → **문헌·검토 단계로 보이나 unknown.**

### 대상 시스템
- AM: **NCM811**, bimodal (D12 / D4 — 원고 초록 표기). CSV 필드로는 `r_AM_P_um`, `r_AM_S_um`
- SE: **Li₆PS₅Cl**, D1 (`r_SE_um`, 관측 0.5 / 500 등 케이스마다 다름)
- 조성 축: `am_wt` / `se_wt` (관측 62/38 ~ 72/28), P:S 비 (`P_S_ratio` 0:10 ~ 5:5)
- 캠페인 라벨: `particulate` 등 (`campaign` 열)

### 관심 물리량과 현재 확보된 값의 범위
`docs/db/section7_10case_sweep.csv` (10 케이스) 기준 —
| 양 | 범위 | 단위 |
|---|---|---|
| `porosity_pct` | 15.0 – 18.9 | % |
| `percolation_pct` | 92.3 – 99.6 | % |
| `sigma_ionic_mScm` | 0.117 – 0.173 | mS/cm |
| `sigma_e_mScm` | 3.18 – 4.63 | mS/cm |
| `sigma_th_mScm` | 3.42 – 4.33 | mS/cm |
| `AM_percolation_pct` | 92.3 – 99.7 | % |
| `total_severe_pct` (파괴) | 0.0 – 1.23 | % |
| `AM_AM_CN_mean` | 2.73 – 3.86 | — |
| `SE_SE_CN_mean` | 4.39 – 5.24 | — |
| `tau_Lap_eff` | 1.21 – 4.39 | — |
| `F_DEM_AM_P_AM_P_mN` | 1.32 – 9.04 | mN |
`all_dem_porosity.csv` · `validation_all_cases.csv` — **80 케이스**, porosity 실측 vs 예측 + residual
(관측 porosity 16.4 – 19.7 %, residual −2.91 ~ +1.52 %p)

### 방법론적 쟁점 (원고 §6 소제목이 곧 쟁점 목록이다)
- **1000× 연화 탄성계수**에서의 strain-faithful 준정적 압축 — 왜 타당한가
- **Hooke vs Hertz 접촉모델 등가성** (원고 §6.4)
- Auerbach + **Lawn** 단계별 파괴 분류기, 접촉별 fracture factor
- **Stage E grain 보정** — Cronau 2021/2022 (SE 크기 비정질화), Trevisanello 2021 (AM 결정성),
  Wang 2022 (AM grain 포논 산란)
- **high-contrast Laplacian** (같은 그래프에서 인자비가 20× 벌어짐) → **7-layer defence**
  (adaptive boundary conductance → spsolve sanity → CG retry → ratio guard → 이상치 필터 →
  **Bruggeman EMT fallback** → …), Bruggeman 이 왜 건전한 상한인가 (§6.7)
- **SE–SE grain-boundary 저항의 처리** (§6.6)
- **regime 밖 편차를 fit 하지 않는다** (§6.2) — 물리 우선 porosity 예측
- trust audit: `validation_flags` 자기보고 카드, 케이스별 게이트 통과 여부

### 진행 중 / 끝난 것
- 진행: 원고 `docs/paper/main.tex` (§5 Results / §6 Discussion 작성됨, §7 Conclusion 있음),
  공저자 편집 시트(`docs/reviews/` — 최근 30일 477개 파일 변경), LHS 스윕(8개 미실행 판정),
  SDCP 전도도 판별 팔 사전등록, litdb 흡수 CL-60~CL-65
- 끝난 것: 80–82 케이스 porosity 검증, PCA 분산 분해, Stage E 전 케이스 재실행

### 이 축과 무관한 논문의 특징 (오탐 감축용)
- 액체 전해질 슬러리 코팅·건조, 파우치셀 사이클 수명만 보고하는 실험
- 셀 레벨 BMS·열관리·팩 설계, SOC/SOH 추정
- 순수 합성·소결 실험 (미세구조 정량 없이 XRD·SEM 사진만)
- 원자 스케일 전용 계산 (DFT 밴드구조·NEB) — **그건 축 B 다. 축 A 로 채점하지 말 것**
- 상평형·CALPHAD, 전산유체(CFD), 전극 없는 순수 분말 유동 연구
- Zn·Na·K 이온, 슈퍼커패시터, 연료전지

---

## 축 B (DFT / MLIP) — 브랜치 `claude/friendly-meitner-lldvar`

**한 줄**: 황화물 SE(Li₆PS₅Cl 계열)의 전자구조·탄성·이온수송을 제일원리와 MLIP-MD 로 정량하고,
LiNiO₂ 계면 위 바인더 조각의 흡착 대비와 SEI 상의 Li 이동 장벽을 **보고량을 먼저 정의하고**
사전등록·게이트로 관리하며 계산한다.

### 쓰는 도구·코드 (repo 경로)
- **VASP 외주 번들**: `tools/sdcp/vasp_handoff_bundle.py` (생성기 + 배포 분석기 + 러너 + 봉인,
  ~20k줄 단일 파일), `tools/sdcp/vasp_cost_estimate.py` (비용·makespan 모형),
  `tools/sdcp/c12_prereg_amend_kconv.py` · `c12_render_send_mail.py` · `c12_make_identity.py`
- **QE**: `tools/sei/` (`collect_neb.py`, `watch_qe_relax.sh`) — pw.x relax + neb.x CI-NEB
- **MLIP**: `tools/modelc_v3/`, `tools/ionic/` — UMA-s-1p1(omat) Langevin NVT MD
- **BVSE**: `tools/comp1_v3/` — softBV 기반 이온 경로 프록시
- **ORCA**: `tools/sdcp/run_orca_stage_a.sh` (r2SCAN-3c Opt, SDCP 올리고머 Stage A)
- **거버넌스**: `db/governance/decisions.json` (보고량·게이트 결정 원장), `db/properties/*_prereg_*.json`
  (사전등록), `db/properties/canonical_registry.json` (화면 정본값 단일 출처)
- **위키·문헌**: `kb/` (관리 문서 351개, `tools/kb_wiki.py` 로 index/lint), `litdb/` (digest 208편)
- `webapp/` (Flask, `webapp/data.py` 가 canonical_registry 에서만 숫자를 읽음)

### 대상 조성·계면
- **Li₆PS₅Cl 계열**: `comp1`~`comp5`, `modelc` (= LPSCl1.6), `+B₂O₃`, `LPSOCl` (+O 치환), Nd 치환
- **계면**: LiNiO₂(104) 슬랩(192원자) × 바인더 조각 — **SDCP(설폰화 전도성 고분자) vs PTFE(C10)**
- **SEI 상**: Li metal(bcc), Li₂S, Li₃N–Nd, Li₂O, Li₃P, Li₃PO₄, LiCl
- **AF-ASSB 원고 쪽**: Li₃N(001), LiC₆(0001) 표면

### 관심 물리량과 현재 확보된 값
`db/properties/canonical_registry.json` — 정본 항목 **39건**. 기계 판독 가능(JSON, `source_path` +
`source_key` 로 원자료를 가리키고 `webapp/canonical.py` 가 대조).
| 양 | 값 / 범위 | 상태 |
|---|---|---|
| Band gap (fixed-occ nscf 고유값) | 2.066 (comp1) · 2.099 (modelc) · 1.9671 (+B₂O₃) · 2.2309 (LPSOCl) eV | canonical |
| B₀ (BM3 EOS) | 21.71 – 26.233 GPa | canonical |
| 탄성 (relaxed-ion) | 20.03 – 35.04 GPa | canonical |
| MD 활성화에너지 Ea (멀티시드) | 0.197 eV / (단일시드 앵커) 0.1512 – 0.2867 eV | canonical + provisional |
| ICOHP (LOBSTER, 결합당) | −5.913 – −6.04 eV | canonical |
| SDCP wave1 ΔE(site) | 9.265 – 49.767 meV | canonical |
| SDCP wave1 E_ads (box24) | −0.3302 – −0.7728 eV | provisional |
| NEB Li 이동 장벽 (`db/properties/sei_neb.json`) | Li metal 0.0806 · Li₃Nd 0.229 · Li₂S 0.305 eV | **전부 `provisional_single_cell` · citable=false** |
| 표면에너지 γ_SE (`adhesion.json`) | 0.45 – 1.211 J/m² | — |
- ⚠ **아직 값이 없는 것**: C-12 ΔE_ads (SDCP vs PTFE 조각 대비) — 외주 VASP 16잡이 아직 발송 전이다.

### 방법론적 쟁점
- **Band gap 은 fixed-occupations nscf 의 VBM/CBM 고유값만 인정** — DOS-threshold 판독 금지(~0.3 eV 과소)
- **UMA 를 Li₃N 에 사용 금지** (2026-06 결정론적 편향 판정). LPSCl 계열 MD 에는 검증된 표준
- MLIP-MD: **MSD 창 2–50 ps 고정**, 아레니우스 600/800/1000 K 3점, Nernst–Einstein(Haven=1),
  **σ 절대값 인용 금지 · 비율도 멀티시드 판정만** (단일시드 1.33× 철회 사례)
- BVSE 정량·순위는 **원본 주기셀 값만** (큐빅 박스는 표시용)
- NEB: 전하 규약이 상의 `electronic_class` 로 갈린다 (insulator = V_Li⁻ + jellium / metal = 중성 공공).
  **jellium 은 유한셀 근사 — 셀 수렴 확인 전에는 상 사이 비교 전용**
- **POTCAR 신원**: `post_hoc` 정책이라 이 묶음 결과는 **원고 인용 자격이 없다** (탐색용)
- **보고량을 계산 전에 정의한다** (`kb/templates/estimand_card.md`) — SDCP 흡착에너지를 여덟 번 계산하고
  여덟 번 반려된 뒤 채택. admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 미정의
- **마감 조건을 먼저 박는다** (`db/properties/<계>_closed_<날짜>.json`)
- 계산 조건이 아니라 **상태 선택 정책**을 맞춰야 한다 (NUPDOWN 제약 vs 자유 — 제약된 기준에서
  자유로운 복합체를 뺀 실측 사고)

### 진행 중 / 끝난 것
- 진행: **C-12 외주 VASP 번들** (v34 내부 6렌즈 리뷰 NO-GO → v35 준비 · `runs/sdcp_c12_2026_08_30/`),
  SDCP polaron Stage A (ORCA gs0–gs2 완료, gs3–gs6 대기), SEI NEB 병합(li_metal CI-NEB 완료),
  Cu–Zn convex hull 보고량 카드(계산 전), Nd 치환 조사
- 끝난 것: `db/properties/sdcp_neutral_closed_2026_08_28.json` (마감 선례), LPSCl 밴드갭·탄성·ICOHP 정본화

### 이 축과 무관한 논문의 특징 (오탐 감축용)
- 입자 패킹·압축·DEM·유한요소 미세구조 — **그건 축 A 다**
- 셀 조립·캘린더링 공정 최적화, 파일럿 라인 스케일업
- 계산이 전혀 없는 순수 실험 합성·전기화학 (cycling curve 만)
- 액체·폴리머 전해질 전용, 리튬-공기/황(황화물 SE 아닌 Li–S), Zn/Na/K 이온
- 머신러닝이되 **원자 스케일 퍼텐셜이 아닌** 것 (제조 파라미터 회귀, 이미지 분할 only)
- DFT 이되 배터리와 무관한 계 (촉매, 태양전지, 열전)

---

## 그 외 축
- **세미나·발표**: `kb/seminars/`, `kb/papers/lpscl_vs_lpscl16_seminar_v1.pptx` 등 — 축 B 자료로 만든
  그룹미팅/세미나 산출물. 별도 연구축이라기보다 축 B 의 전달 형태.
- **실험 협업**: `docs/collab/`, AF-ASSB(AgNO₃–C–PVP) 원고 SI 기여. 계산이 실험 원고의 SI 를 받치는 관계.
- **웹앱**: 양 브랜치 모두 Flask 웹앱을 갖고 있다 (축 A 케이스 브라우저 / 축 B 정본값 뷰어).

---

## 논문 원고 현황

| 축 | 경로 | 제목 | 섹션 | 진행률 | 타깃 저널 |
|---|---|---|---|---|---|
| A | `docs/paper/main.tex` (브랜치 B) | Stage E fracture-aware network solver for all-solid-state battery cathode microstructure: a literature-grounded multi-physics framework with 7-layer defence and Bruggeman fallback | Introduction / Methodology (DEM particle configuration · Contact-network extraction and Kirchhoff solve · Three parallel transport channels) / Stage E literature-grounded grain corrections / 7-Layer defence and Bruggeman fallback / Results (Pipeline self-consistency · Trust audit · Variance decomposition · Cell-level ASR validation · Design rule AM_P fraction vs σ_e loss · Strict physics-first porosity prediction) / Discussion (Two competing densification mechanisms · Why we do not fit out-of-regime deviations · Limitations · Hooke–Hertz equivalence · SE–SE grain boundary · Bruggeman upper bound · Porosity wave-shape sensitivity · Stress-bearing percolation) / Conclusion | 본문 1034행+ 전 섹션 초안 있음 · 공저자 편집 시트 진행 중 | **unknown** (refs.bib 만 있고 저널 지정 문구 없음) |
| A | `docs/manuscript/Methods_simulation_v7_for_coauthors.docx` | 공저자용 시뮬레이션 Methods v7 | unknown (.docx) | 정본 rev7 | unknown |
| B | `docs/manuscripts/Methods_DFT_v9_for_coauthors.docx` · `Methods_simulation_v8_for_coauthors.docx` · `Table_S2_DFT_parameters.docx` · `Figure2e_explained_v10.docx` | **AF-ASSB AgNO₃–C–PVP 원고 (v5)** 의 Methods·SI 기여 | SI Table S2 = Li₃N(001)/LiC₆(0001) DFT 파라미터 | SI v6 제출본 형태 확정 (`--nonotes`) | unknown |
| B | `kb/papers/draft_v1.md`, `computational_methods_draft.md` | 내부 초안 | — | unknown | unknown |

> `use_in_my_paper` 를 쓸 때: 축 A 는 **main.tex 의 절 이름으로** 지목할 수 있다 (예: "§6.6 SE–SE
> grain-boundary 문단에 인용"). 축 B 는 원고가 .docx 라 절 지목이 어렵다 — `kb/` 카드나
> `db/properties/` 항목으로 지목하는 편이 정확하다.

---

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
- 축 A 핵심: `discrete element`, `DEM`, `LIGGGHTS`, `MPM`, `material point method`, `voxel`,
  `resistor network`, `percolation`, `Kirchhoff`, `Bruggeman`, `constriction resistance`,
  `effective medium`, `tortuosity`, `Heckel`, `coordination number`
- 축 B 핵심: `first-principles`, `DFT`, `density functional`, `ab initio`,
  `machine learning potential`, `MLIP`, `AIMD`, `NEB`, `nudged elastic band`, `COHP`, `ICOHP`,
  `LOBSTER`, `bond valence`, `BVSE`, `band gap`, `VASP`, `Quantum ESPRESSO`
- 공통 시스템: `all-solid-state`, `sulfide`, `Li6PS5Cl`, `LPSCl`, `argyrodite`, `halide electrolyte`,
  `composite cathode`, `NCM811`, `NMC811`
- 물성·공정: `porosity`, `tortuosity`, `compaction`, `calendering`, `contact`, `elastic`, `modulus`,
  `adhesion`, `interface`, `NCM`, `ASR`, `area specific resistance`, `binder`, `PTFE`, `PVDF`
- 감점: `supercapacitor`, `zinc-ion`, `sodium-ion`, `fuel cell`, `photocatal`, `perovskite solar`,
  `redox flow`, `thermoelectric`, `hydrogen storage`, `CALPHAD`, `battery management`,
  `state of charge estimation`
- 프리프린트(arXiv 등)는 IF 0 — relevance만으로 tier 결정

## 심층 분석 시 반드시 채울 항목 (형식은 고정)
1. 비교 가능한 **수치** — 단위와 조건 포함
2. **방법론 세부** — 해당 축의 계산 조건
   (축 A: 접촉 모델·강성·마찰·압축압력·입경분포·셀 크기 / 축 B: functional·k-point·supercell·U 값·
   MLIP 학습 데이터·앙상블·MSD 창)
3. **내 결과와의 일치/충돌** — 위 "확보된 값" 표와 대조. ⚠ 축 B 의 NEB·E_ads 는 아직
   `provisional` 이므로 "우리 값과 일치" 라고 쓰지 말고 "우리 잠정값과 같은 자릿수" 로 쓴다
4. **인용 포인트** — 축 A 는 `main.tex` 절 이름, 축 B 는 `kb/` 카드 또는 `db/properties/` 항목
5. **비판 포인트** — 세미나 질문·리뷰어 관점

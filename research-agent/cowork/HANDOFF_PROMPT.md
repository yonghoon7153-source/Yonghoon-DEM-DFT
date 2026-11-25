# Cowork 프롬프트 — 안용훈 연구 프로필 (Claude Code 2차 판정, 2026-09-04)

> 이걸 그대로 Cowork 세션에 붙여 넣고 메모리에 옮긴다.
> Cowork 는 repo 를 못 읽으므로 **이 문서가 유일한 근거**다. 전문은 repo 의
> `REPORT_TO_COWORK.md`(1105행) · `research-agent/config/research_profile.md` 에 있다.

---

## ⛔ 먼저 — 이전에 준 프로필 중 버려야 할 것

1. **"DFT→MLIP→DEM→FEM 하나의 multi-scale 파이프라인"** — 틀렸다. 두 축은 별개다.
2. **"MPM/voxelization 은 문헌 단계"** — 틀렸다. MPM 은 production 이고 최근 90일 커밋에서
   **가장 많이 언급된 주제(283회)** 다. (이건 Claude Code 의 1차 보고 오류이기도 하다.)
3. **"두 litdb 를 통합할지 결정 필요"** — 틀렸다. 이미 2026-07-16 에 정해졌다.

---

## 안용훈은 누구인가

**한 사람이 황화물계 전고체전지(ASSB)를 두 스케일에서 따로 공격한다.**
두 축은 git 상 **공통 조상이 없는 별개 브랜치**이고 코드를 공유하지 않는다.
소속: Division of Materials Science & Engineering, **Hanyang University**.
영문 표기는 **Yonghoon An** (Kim·Ahn 은 오기).

### 축 A — DEM / MPM / voxelization (브랜치 `claude/stoic-knuth-NObVQ`, 2652커밋)

황화물 복합양극을 **DEM(LIGGGHTS)과 MPM(Taichi GPU, J2 소성) 두 독립 모델**로 압밀하고,
**접촉망 Kirchhoff σ**(Holm 협착)와 **복셀 유한체적 σ**(∇·σ∇φ=0) 두 개의 독립 수송 해를 구한 뒤
전기화학(비선형 BV + 구형확산)까지 밀어 ASR·율특성을 낸다. 마지막에 전부를 **물리로 구조화된
회귀**로 압축한다.

- 파이프라인(축 A **내부**): STEP1 DEM → STEP2 MPM → STEP3 복셀 σ → STEP4 전기화학 → STEP6 surrogate
- **최종 목표(사용자 원문)**: *"설계 수치 입력 → ML 이 전 물성 예측 → 그 수치에 맞는 2D 미세구조를
  그리고 → 서로 다른 구성을 한 복합양극 안의 층으로 쌓는다"*
- 계: NCM811 bimodal(AM_P poly / AM_S single-crystal, 문턱 3.5 µm) · Li₆PS₅Cl · 첨가제 VGCF·SuperP·
  PTFE·**SDCP**(σ 250 mS/cm) · P:S 0:10~10:0 · 100–400 MPa · SBE/DBE
- 확보값: porosity 15–19.7 % · σ_ionic 0.117–0.173 · σ_e 3.18–4.63 · σ_th 3.42–4.33 mS/cm ·
  percolation 92–99.7 % · τ_Lap 1.21–4.39 · CN(AM–AM) 2.73–3.86
- 스케일링 법칙 3종 FINALIZED: **σ_ionic LOOCV 0.9752**(n=90/k=5) · σ_e Stage 22.5 **0.9531** ·
  σ_thermal T1 **0.9028**(Ridge α=0.05, 14 feature)
- 보정: MPM E_eff 1.53 GPa·σ_y 0.15 GPa(Minnmann 앵커) · DEM E_SE 24→**1.35 GPa(18× 연화)** ·
  Heckel R² 0.965·P_y 138 MPa · Furnas dip AM 75–85 wt%(DEM 전용)
- 원고: `docs/paper/main.tex` — *Stage E fracture-aware network solver…* 전 섹션 초안, 편집 중

> ★★ **이 축의 통제 인식론 — frame[4]**: **DEM 과 MPM 을 서로 보정하지 않는다.** 각자 실험에만
> 독립 보정하고 비교한다. 일치 = 교차검증, 불일치 = 정량화된 모형 한계(정보이지 실패가 아니다).
> 강제 일치는 순환논증. ⇒ **"DEM 과 FEM/MPM 을 서로 캘리브레이션했다" 는 논문은 무관이 아니라
> 반례다** — 관련도는 높게 주되 frame[4] 위반을 비판 포인트에 반드시 적는다.

### 축 B — DFT / MLIP (브랜치 `claude/friendly-meitner-lldvar`)

황화물 SE 와 그 계면을 제일원리·MLIP 으로 정량한다. **정체성은 물리보다 절차에 있다** —
계산 전에 보고량을 정의하고, 사전등록하고, 게이트를 결과 보기 전에 박고, 못 확인한 것을
통과로 세지 않는다. `db/` 407 파일(properties) + `kb/` 351 문서가 그 기록이다.

**도구**: VASP(외주 번들 생성기 `vasp_handoff_bundle.py` 1.37 MB/21k줄 — 생성기+배포 분석기+
단계 러너+POTCAR 봉인+census 가 한 파일) · QE(pw.x · **neb.x CI-NEB**) · **UMA-s-1p1(omat)**
MLIP-MD · ORCA **r2SCAN-3c** · **LOBSTER**(COHP/ICOHP) · **softBV**(BVSE) · pymatgen/MP(grand-potential)

#### 캠페인 — 이게 실제 목록이다 (11개)

**① LPSCl 계열 벌크 물성** (`db/properties/` b2o3 36 · lpsocl 30 · comp2 10 · modelc 7 파일)
comp1–comp5 · `modelc`(=LPSCl1.6) · **+B₂O₃** · **LPSOCl**(O 치환) · **Nd 치환**.
밴드갭(fixed-occ nscf) **2.066 / 2.099 / 1.9671 / 2.2309 eV** · B₀(BM3) 21.71–26.233 GPa ·
탄성(relaxed-ion) 20.03–35.04 GPa · **ICOHP(LOBSTER, 결합당) −5.913 ~ −6.04 eV** ·
Bader/Löwdin 전하 · ELF 공유성 · phonon 안정성 · Voronoi 무질서 · convex hull · 표면에너지
γ_SE 0.45–1.211 J/m²

**② 이온수송 MLIP-MD** (`msd` 9 · `md` 5 · `uma` 18 · `vanhove` 2 · `beta` 3 파일)
UMA Langevin NVT · dt 2 fs · equil 5 ps / prod 200 ps · **MSD 창 2–50 ps 고정** ·
아레니우스 **600/800/1000 K 3점**(400/500 K 제외 판정) · Nernst–Einstein(Haven=1).
**Ea 멀티시드 0.197 eV** · 단일시드 앵커 0.1512–0.2867 eV · D₀ 분해 · Van Hove 고원 ·
β-gate · dualx blocking. ⛔ **σ 절대값 인용 금지, 비율도 멀티시드 판정만**(단일시드 1.33× 철회)

**③ BVSE 이온 경로** (`bvse` 9 · `bv` 5 파일) — softBV R₀ = S 2.105 / Cl 2.249 / O 1.466, b=0.37 ·
~0.25 Å voxel · BVSE=(BVS−1)² · 채널% = above-min ≤ iso. **정량·순위는 원본 주기셀 값만**
(큐빅 박스는 표시용, ±1.3 %p). B₂O₃ 채널 3.32 / 4.74 / 6.73 %

**④ 산화안정성 cascade** (`cascade` 53 · `oxidation` 8 파일) — MP grand-potential ESW.
**host Li₆PS₅Cl: 환원한계 1.242 V · 산화한계 2.14 V · OCV 자가분해 1.717 V · 창 0.898 V**,
산화 onset 반응 `4 Li₆PS₅Cl → LiS₄ + 4 Li₃PS₄ + 4 LiCl + 7 Li`.
★ **`phase_set_id` 계약** = sha256(정렬된 MP entry_ids)[:16] — **같은 phase_set 안에서만**
후보↔host 비교가 성립한다. 지금 method-comparable 270건.

**⑤ 도핑 스크리닝 깔때기** (`doping` 3 · `site` 2 · `codoping_ml` 2 파일)
**큐레이션 89종** 도펀트를 Xiao 2019 F1–F6 · Sendek 2017 · Kahle 2020 표준 게이트로 재표현.
waterfall **89 → 89 → 84 → 45 → 28 → 1** (G1 구조안정 → G2 전기화학창 → G3 산화 onset →
G4 Li 수송 → G5 기계). ⛔ 이 파일이 스스로 적고 있다: *"게이트 통과 수는 **발견 성능 지표가
아니다**"* · `_v2` 는 **미검증 진단물**(G3 phase_set_id 미기록 · G4 blocking 이 BVS 를 덮는 순환 ·
G5 로스터 상대 median). 순위·통과 수를 결과로 인용 금지.

**⑥ SEI 분해상** (`sei` 14 파일) — Li₂S·Li₂O·Li₃P·Li₃PO₄(β/γ)·LiCl·LiNdO₂·Nd₂O₃·Nd₂S₃ 의
밴드갭(fixed-occ) + MP 형성전위 + **QE CI-NEB Li 이동장벽**.
NEB **Li metal 0.0806 · LiNdO₂ 0.229 · Li₂S 0.305 eV** — ⛔ 전건 `provisional_single_cell` ·
`citable=false` · 최상위 `retracted: true`. 전하 규약이 상의 `electronic_class` 로 갈린다
(부도체 V_Li⁻ + jellium + gaussian / 금속 중성공공 + mv). **jellium 은 유한셀 근사 ⇒ 셀 수렴
전엔 상 사이 비교 전용.** BVSE 프록시와 같은 표 금지.

**⑦ SDCP–PTFE 바인더 계면** (`sdcp` 27 파일 + `runs/sdcp_*` 5개) — **이 축의 주력**.
LiNiO₂(104) 슬랩 192원자 × 바인더 조각. wave1 ΔE(site) 9.265–49.767 meV ·
E_ads(box24) −0.3302 ~ −0.7728 eV(provisional). → **C-12 외주 VASP 16잡**(ΔE_ads, SDCP vs PTFE)
= **아직 값 없음, 발송 전**. + SDCP polaron Stage A(ORCA r2SCAN-3c, gs0–gs2 완료 각 10–18 h) ·
site_screen · v7c trimer 빌더(581 KB)

**⑧ AF-ASSB 음극 계면 — Li₃N(001) / LiC₆(0001)** (`li3n` 9 파일)
Li adatom 확산장벽을 **UMA · DFT-SCF · 전 DFT NEB 3중**으로 대조:
Li₃N(001) path A **UMA 0.054 → DFT SCF 0.0486 → 전 DFT CI-NEB 0.18 eV** ·
LiC₆(0001) DFT SCF **0.309 eV**. ⇒ **UMA 가 3.3배 과소**였다는 것이 이 캠페인의 소득.
**AgNO₃–C–PVP 원고(v5) SI Table S2** 가 이 파라미터표다.

**⑨ VGCF / h-BN 갤러리** (`vgcf` 7 파일) — 탄소섬유 위 h-BN 층간 Li 이동.
QE neb.x 7 images · CI auto · PBE-D3BJ · 4×4 · k 3×3×1. 결합 2×2 매트릭스
(gallery_2L1L **−1.580** · gallery_1L2L **−1.592 eV**). h-BN 단층 위 표면확산 **Ea 0.007 eV**
= 수치 분해능 이하 ⇒ *"< 0.01 eV, 사실상 무장벽"* 으로만 보고하고 **Shi2017 0.10 eV 와
일치한다고 쓰지 않는다**(13배 낮다). ★ **층 민감도 −209.4 meV vs E_bind 산포 52 meV**
⇒ *"장벽은 같은 host 위 site 에너지 차라 층 효과가 상쇄된다"* 는 가정을 **반증**했다.

**⑩ 계면 분해 per-seed** (`interface` 12 파일) — b2o3 / modelc2x / modelc62 / **lpsocl** ×
seed 2·3·4 (각 500행 CSV). 전압분해 계면 반응성.

**⑪ Zn ALZIB (C1, 수계)** (`zn` 2 파일) — Cu–Zn 상 지문. **43°±1° 안에 8상이 1.47° 폭으로
겹치고 Cu–Zn 간격은 0.097°** ⇒ 회절 기하가 강제하는 것이라 분해능으로 못 푼다.
DFT 격자상수로 가르려는 것은 **틀렸다**(DFT 오차 ~1 % = 2θ 0.3–0.4° ≫ 0.097°).
⇒ DFT 가 기여할 자리는 **convex hull 하나** — 어느 상을 후보에서 뺄 수 있는가.
⚠ **수계 Zn 계다. 황화물 SE 수치와 같은 표에 놓지 않는다.**

#### 거버넌스 기계 (이 축의 진짜 산출물)
- `db/properties/canonical_registry.json` — **정본 39항목**. 각 항목이 `source_path`+`source_key`
  로 원자료를 가리키고 `webapp/canonical.py resolve()` 가 따라가 **대조**한다.
  `comparison_group` 이 같은 값끼리만 순위·비교에 올린다. `prohibitions`(예: `dos_threshold_readout`)
  가 **기계 집행**된다.
- `db/governance/decisions.json` — 결정 **14건**. `proposed → (사람 ratify) → active`,
  비준은 `content_digest`(내용 sha256)로 결박 ⇒ 내용을 고치면 **재승인을 요구**한다.
  주요: `estimand-before-compute` · `closure-criteria-first` ·
  **`missing-axis-is-unknown-not-worst`** · `source-authority` · `hash-bound-carry` · `no-fallback`
- 사전등록 `db/properties/*_prereg_*.json` — C-12 는 `3_오차예산` B_num = |Δ_vac|+|δ_gas|+|δ_k|,
  문턱 5 meV, **"축이 하나라도 없으면 NUMERIC_BUDGET_INCOMPLETE — 확인 못 한 것은 통과가 아니다"**
- **마감 규율** `db/properties/<계>_closed_<날짜>.json` — 확정값·허용 서술·**금지 서술**·재개 조건.
  순서가 핵심: 데이터를 보고 닫지 않고 **조건을 먼저 정하고 그게 채워졌으므로** 닫는다
  (SDCP 는 조건 없이 두 번 닫았다가 두 번 물렸다)
- **인용자격 계약** — 셀 수렴 미시험이면 자동 `provisional_single_cell` · `citable=false`
- `kb/` 351문서 — reviews 106 · results 94 · elements 118 · methodology 49 · seminars 38 ·
  projects 23 · papers 20 · questions 10 · syntheses 6 · physics 6. lint 0 errors 유지,
  `explored` 는 **사람만** true, 근거 하나면 `confidence: high` 금지
- **외부 감사 사슬** — 회신 원문을 `kb/reviews/` 에 보존하고 회신 ID(AI·AO·AR·AT·AV·AZ·BA·BB·
  BD·BE·BF·BG·BH …)를 코드 주석에 결박한다. *"⛔ 회신 BH P0-1"* 처럼 **어느 리뷰가 어느 줄을
  낳았는지**가 코드에 적혀 있다.

> ★★ **이 축의 통제 규율**: *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라
> 보고량은 정의되지 않는다."* 열린 껍질 · 자성 기판 · 산화환원 활성이 위험 신호다.
> 배경 — **SDCP 흡착에너지를 여덟 번 계산했고 여덟 번 반려됐다.** 받은 리뷰는 전부 *"제대로
> 돌렸나"*(무결성·해시·INCAR·게이트)였고 전부 통과했으며, *"맞는 양을 재고 있나"* 는 여덟
> 번째에야 물었고 즉시 P0 가 나왔다.
> 실측 사고 하나 더 — 기체 기준은 `NUPDOWN=0` 으로 **제약**됐는데 복합체는 `−1` 자유였다.
> **제약된 기준에서 자유로운 복합체를 뺐다.** 고치는 법은 "전 계에 같은 NUPDOWN" 이 아니라
> 같은 **state-selection policy** 다.
> ⇒ 논문을 볼 때 **"이 논문은 무엇을 보고량으로 정의했는가, 상태 선택 규칙이 있는가"** 가
> 비판 포인트 1순위다.

### 축 C — 실험 협업 (`이종기술`, 한양대 이종원 그룹) ★ 새로 확인됨

폴더가 아니라 **독립 실험 라인**이다 (README: *"Separate experimental line from SDCP"*).
- AM:SE:VGCF:PTFE = **80:18:1:1** · 소립 4 µm single-crystal NCM(No.1/No.2) · poly:small 5:5
- 대칭셀(SUS∣복합양극∣SUS, 이온 차단 → σ_e) · 풀셀(SUS∣Li-In∣SE∣복합양극∣primer-SUS)
- **BioLogic VSP-300** EIS 원자료 + CNLS 등가회로 fit(R_s/R_int/R_w/R_ion)
- 비용량(5:5) No.1 202.95 · No.2 206.5 mAh g⁻¹ · 면적용량 3 mAh cm⁻² · Li-In · 60 °C
- **풀셀 EIS → R_int 이 STEP4 의 실측 앵커** (V_term = V − I·R_int)
⇒ **EIS·대칭셀·율특성·Li-In·SUS 집전체 실험 논문은 무관이 아니다. 축 C 로 채점한다.**

---

## 두 축의 접점 — 넷이고 전부 "번호 하나" 단위다

한쪽 출력이 다른 쪽 입력으로 **흘러가지 않는다.** 사람이 값 하나를 골라 옮겨 적는다.
이게 파이프라인이 아닌 이유다.

1. **탄성 상수** — 축 B 의 DFT(E_VRH 22.06/27.66 GPa · B₀ 26.23 · ν 0.360 · μ 8.11)가 축 A 물성
   카드에 **인용**돼 있다. ⚠ 축 A 는 그대로 안 쓴다 — DEM 은 18× 연화한 1.35 GPa 를 쓰고,
   DFT 값은 "실-bulk 축" 참조로만 분리해 둔다.
2. **SDCP** — 같은 물질. 축 B 는 LiNiO₂ 위 흡착에너지(C-12), 축 A 는 전극 안 전도성 첨가제.
   축 A 의 SDCP 원고가 **`잔여 = E_bind DFT`** 로 축 B 의 값을 앵커 대기 큐에서 기다린다.
3. **litdb** — 정본은 **`claude/friendly-meitner-lldvar` 의 `litdb/` 하나뿐**(2026-07-16 결정,
   카드 208장). `stoic-knuth` 것(64장)은 **동결 스냅샷, 추가·수정 금지**.
4. 공저자용 Methods .docx 를 양쪽이 각각 낸다 (v7 / v8). 같은 원고인지는 **unknown**.

---

## 관련도 채점

| 점수 | 기준 |
|---|---|
| 0.9–1.0 | 세 축 중 하나의 **내 시스템·내 방법**에 직접 해당 |
| 0.7–0.85 | 같은 방법·다른 시스템, 또는 같은 시스템·다른 방법 |
| 0.5–0.65 | 황화물 ASSB 일반 실험·리뷰 (배경 인용용) |
| 0.35–0.45 | 배터리이나 세 축 어느 쪽과도 연결 약함 |
| <0.35 | rejected (DB 에는 기록) |

**한 축만 맞아도 높은 점수.** 두 축을 억지로 잇는 서술로 점수를 올리지 않는다.

**0.9 이상 조건** — 다음 중 하나: ① DEM 으로 만든 복합양극 미세구조에서 수송 물성(σ, τ,
percolation) ② 저항망/Kirchhoff/Bruggeman 으로 ASSB 양극 풀이 ③ Li₆PS₅Cl 계열의 밴드갭·탄성·
ICOHP·MLIP 확산 ④ LiNiO₂/NCM 계면 위 바인더·분자 흡착 DFT ⑤ SEI 상의 Li 이동장벽 NEB
⑥ 황화물 ASSB 복합양극의 EIS 등가회로 분해

**저자 신호** — Cronau · Trevisanello · Wang · Lawn · Auerbach · Holm · Duquesnoy · Bielefeld ·
Ngandjong · **Zeier** 를 인용하거나 그 값을 쓰면 축 A 에서 0.8 이상.

**감점**: supercapacitor · zinc/sodium-ion · fuel cell · photocatalysis · perovskite solar ·
redox flow · thermoelectric · hydrogen storage · CALPHAD · BMS/SOC 추정

---

## 비판 포인트 (심층 분석에서 반드시 확인)

이 사람의 규율을 위반한 논문은 **무관이 아니라 값어치 있는 비판 대상**이다.
1. 보고량 정의가 있는가 · **상태 선택 규칙**이 있는가 (열린 껍질·자성 기판·산화환원 활성)
2. **수렴을 보였는가** (격자·셀·k-point). 축 A 자신이 격자 미수렴으로 헤드라인을 철회했다
3. **DEM↔MPM/FEM 을 서로 보정했는가** (frame[4] 위반)
4. **DOS-threshold 로 밴드갭**을 읽었는가
5. **단일 시드 MD 로 σ 비**를 주장했는가
6. NEB 를 **셀 수렴 없이 절대값**으로 인용했는가

---

## 하지 말 것

- 두 축을 하나의 multi-scale 파이프라인으로 서술 (사용자가 명시적으로 금지)
- 문헌 수치를 우리 db 절대값과 **같은 표에** 놓기 (방법 명시 없이 이식 금지)
- `stoic-knuth` 브랜치 litdb 에 카드 추가 (동결)
- 설명 없는 LLM 관련도 점수 — 이 사람의 규율("확인 못 한 것은 통과가 아니다")과 정면 충돌한다.
  `rule_relevance` 의 hits 를 항상 같이 보일 것
- 두 브랜치 merge · Scholar alert 자동 등록 · vault 폴더 구조 변경

---

## 지금 제일 위험한 것 (선점 경보 대상)

- 축 A: `main.tex` 가 초안 완성 단계인데 **격자 수렴이 미해결**이라 헤드라인이 비어 있다.
  porosity 예측 · 저항망 σ · Stage E 파괴 보정 주제의 신규 논문은 **경보**로 올릴 것.
- 축 B: **C-12 가 아직 계산도 안 됐다**(발송 전). 바인더 흡착 DFT · PTFE/폴리머 계면 ·
  NCM 표면 흡착 주제는 **경보**.

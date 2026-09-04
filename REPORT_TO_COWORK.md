# REPORT_TO_COWORK

> Claude Code → Cowork(클라우드). 클라우드는 repo 를 못 읽으므로 **이 문서가 유일한 전달 경로**다.
> 작성 2026-09-04 · 브랜치 `claude/friendly-meitner-lldvar` @ f6194e2cf · 대조 `claude/stoic-knuth-NObVQ` @ 047746866
>
> **규칙**: 추측 금지. 근거 없는 칸은 `unknown`. 원문은 요약하지 않고 그대로.
>
> ⚠ **먼저 알아야 할 사실 하나** — `git merge-base claude/friendly-meitner-lldvar claude/stoic-knuth-NObVQ`
> 가 **rc=1, 출력 없음**이다. 두 브랜치는 **공통 조상이 아예 없는 별개 히스토리**다. Cowork 가
> "DFT→MLIP→DEM→FEM 하나의 파이프라인" 이라고 쓴 것은 틀렸고, 사용자 정정이 맞다.

---

## 1. 브랜치 A (`claude/friendly-meitner-lldvar`) 가 본 연구자

### A-1 무엇을 연구하는가
황화물계 고체전해질(Li₆PS₅Cl 계열)의 **전자구조·탄성·이온수송을 제일원리와 MLIP 으로 정량**하고,
**LiNiO₂ 계면 위 바인더 조각의 흡착 대비**와 **SEI 상의 Li 이동 장벽**을 계산한다. 특징은 물리보다
**절차**에 있다 — 보고량을 계산 전에 정의하고(`kb/templates/estimand_card.md`), 사전등록하고
(`db/properties/*_prereg_*.json`), 결정을 원장에 등록하고(`db/governance/decisions.json`),
게이트를 결과 보기 전에 박는다.

근거:
- `tools/sdcp/vasp_handoff_bundle.py` — VASP 외주 번들 생성기 + 배포 분석기 + 러너 + POTCAR 봉인 (단일 파일 ~21k줄)
- `db/properties/canonical_registry.json` — 화면 정본값 39건의 단일 출처
- 커밋 `f6194e2cf` "C-12: INCAR 에 KPAR 명시", `9be615eca` "kb/reviews: C-12 v34 내부 6렌즈 리뷰 종합 — NO-GO"
- `CLAUDE.md` §"계산 규율 — 던지기 전에 보고량 정의 (2026-08-28 채택)" — *"SDCP-doped 흡착에너지를
  **여덟 번** 계산했고 여덟 번 반려됐다. 받은 리뷰는 전부 '제대로 돌렸나'였고 전부 통과했다.
  '맞는 양을 재고 있나' 는 여덟 번째에야 물었고 즉시 P0 가 나왔다."*
- 원고 기여: `docs/manuscripts/` — **AF-ASSB AgNO₃–C–PVP 원고(v5)** 의 Methods·SI

**목적 한 줄**: 원자 스케일 계산을 원고에 인용 가능한 상태로 만드는 것. 그리고 그 자격을 기계가 집행하게 하는 것.
**활동 기간**: 이 브랜치 커밋 기준 최근 활동 2026-09-03 (조사 시점 최신).

### A-2 연구 축
이 브랜치에는 **축이 하나**다 — 축 B (DFT/MLIP). 축 A(DEM)는 **문헌으로만** 존재한다
(`litdb/INDEX_DEM.md`, `litdb/comparison_vs_ours_DEM.md`, duquesnoy2020 calendering voxel digest).
즉 이 브랜치의 연구자는 DEM 을 **읽지만 돌리지는 않는다.**

| | 축 B (DFT / MLIP) |
|---|---|
| 도구·코드 | `tools/sdcp/vasp_handoff_bundle.py` · `vasp_cost_estimate.py` · `c12_*.py` (VASP) / `tools/sei/collect_neb.py`·`watch_qe_relax.sh` (QE pw.x·neb.x) / `tools/modelc_v3/`·`tools/ionic/` (UMA MLIP-MD) / `tools/comp1_v3/` (BVSE) / `tools/sdcp/run_orca_stage_a.sh` (ORCA r2SCAN-3c) / `tools/kb_wiki.py` (kb 위키) / `webapp/` |
| 대상 시스템 | Li₆PS₅Cl 계열 (comp1–comp5 · modelc=LPSCl1.6 · +B₂O₃ · LPSOCl · Nd 치환) · LiNiO₂(104) 슬랩 192원자 × 바인더 조각(SDCP vs PTFE C10) · SEI 상(Li metal · Li₂S · Li₃N–Nd · Li₂O · Li₃P · Li₃PO₄ · LiCl) · Li₃N(001)·LiC₆(0001) |
| 관심 물리량 | band gap · B₀ · 탄성계수 · MD 활성화에너지 · ICOHP · ΔE_ads · NEB 장벽 · 표면에너지 |
| 방법론 쟁점 | DOS-threshold 판독 금지 · UMA 를 Li₃N 에 금지 · MSD 창 2–50 ps 고정 · 단일시드 비율 인용 금지 · jellium 유한셀 근사 · POTCAR post_hoc → 원고 인용 자격 없음 · 상태 선택 정책(NUPDOWN) |
| 진행 상태 | C-12 외주 번들 v34 **NO-GO** → v35 준비 (진행) · SDCP polaron Stage A ORCA (gs0–gs2 완료, gs3–gs6 대기) · SEI NEB 병합 (li_metal 완료) · Zn hull 카드 (계산 전) |

### A-3 산출물 인벤토리
| 종류 | 경로 | 한 줄 | 상태 |
|---|---|---|---|
| 시뮬레이션 케이스 | `runs/sdcp_c12_2026_08_30/` | C-12 외주 VASP 번들 v31–v34 (zip 동봉) | v34 발송 금지 표기 |
| | `runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/OUTCAR.gz` | 비용 모형의 실측 기준선 (192원자·48코어·525 s/전자스텝) | 완료 |
| 후처리 코드 | `tools/` (py 305 · sh 106 · 62k줄) | 도구 전반 | — |
| 정본 수치 | `db/properties/` 377개 파일 · `canonical_registry.json` 39항목 | 화면·원고가 읽는 단일 출처 | canonical / provisional / retracted 로 상태 표기 |
| 거버넌스 | `db/governance/decisions.json` (결정 14건) | 보고량·게이트 결정 원장 (proposed→ratified) | — |
| 논문 원고 | `docs/manuscripts/Methods_DFT_v9_for_coauthors.docx` · `Methods_simulation_v8_for_coauthors.docx` · `Table_S2_DFT_parameters.docx` · `Figure2e_explained_v10.docx` | **AF-ASSB AgNO₃–C–PVP 원고(v5)** Methods·SI 기여 | SI v6 제출본 형태 확정 |
| 문헌 DB | `litdb/` — `papers/*.md` **208편** · `INDEX.md` · `INDEX_DEM.md` · `topics.json` · `pdf_map.tsv` | Markdown digest 체계 | 활발 |
| 위키 | `kb/` 관리 문서 **351개** (`kb/reviews/` · `kb/methodology/` · `kb/physics/` · `kb/questions/` · `kb/syntheses/` · `kb/seminars/`) | lint 0 errors 유지 | 활발 |
| 스킬·에이전트 | `.claude/agents/litdb-curator.md` · `.claude/commands/{daily,kb-lint,kb-new}.md` | 논문 digest 자동화 등 | — |

### A-4 살아있는 것 (최근 30일)
1. **C-12 외주 VASP 번들** — v31→v34 반복, 내부 6렌즈 리뷰가 v34 를 NO-GO. P0 두 건: 선택
   attestation 이 실물에서 1단계 게이트를 막는다 / δ_k 축 설계 제외가 비준 사전등록과 어긋난다.
2. **KPAR / 비용 모형** (2026-09-04, 오늘) — INCAR 에 KPAR 이 없어 k 병렬이 안 걸렸고 비용 모형이
   코어 확장을 과대평가했다. 외주처 큐 상한 91시간 판정이 여기 걸려 있다.
3. **SDCP polaron Stage A** (ORCA r2SCAN-3c) — gs0–gs2 완료(각 10–18시간), gs3–gs6 대기.
4. **SEI NEB** — li_metal CI-NEB 완료(0.0806 eV), 다중 기계 루트 병합.
5. **Zn / Cu–Zn convex hull 보고량 카드** — 계산 전, 사용자 §3 승인 대기.

TODO·미결:
- δ_k 재개 조건 A/B/C 중 1저자 결정 대기 → 이게 v35 를 막는 유일한 블로커
- Polaron S0 사전등록 재비준 (status: proposed)
- `db/properties/sei_neb.json` — `retracted: true` (인용 가능 0/9)
- 결과는 났는데 원고에 안 들어간 것: NEB 세 값(0.0806 / 0.229 / 0.305 eV)은 셀 수렴 미시험이라
  `provisional_single_cell`, 상 사이 비교로만 쓸 수 있다

### A-5 확보된 수치 — **원자 스케일 계열**
**형식: JSON, 기계 판독 가능.** `db/properties/canonical_registry.json` 의 각 항목이
`source_path` + `source_key` 로 원자료를 가리키고 `webapp/canonical.py` 의 `resolve()` 가 따라가 대조한다
(`tools/db/validate_canonical.py`). **스크립트에 흩어져 있지 않다.**

| 물리량 | 값 / 범위 | 단위 | 경로 | 상태 |
|---|---|---|---|---|
| Band gap (fixed-occ nscf 고유값) | 2.066 · 2.099 · 1.9671 · 2.2309 | eV | `db/properties/electronic.json` · `lpsocl_dos_gap.json` | canonical |
| Band gap (legacy DOS-threshold) | 2.04 | eV | 같은 파일 | **provisional · 인용 금지** |
| B₀ (BM3 EOS) | 21.71 – 26.233 | GPa | `eos.json` · `lpsocl_eos_dft_result.json` · `b2o3_eos_dft_result.json` | canonical |
| 탄성계수 (relaxed-ion) | 20.03 – 35.04 | GPa | `elastic.json` | canonical |
| MD 활성화에너지 (멀티시드) | 0.197 | eV | `b2o3_vs_lpscl16_conductivity.csv` | canonical |
| MD 활성화에너지 (단일시드 앵커) | 0.1512 – 0.2867 | eV | `lpsocl_md_arrhenius.json` · `comp2_*.json` · `li_transport.json` | provisional |
| ICOHP (LOBSTER, 결합당) | −5.913 – −6.04 | eV | `lpsocl_icohp.json` · `b2o3_icohp.json` · `nd_icohp.json` · `per_bond_json/` | canonical |
| SDCP wave1 ΔE(site) | 9.265 · 36.071 · 36.157 · 49.767 | meV | `sdcp_wave1_citable.json` | canonical |
| SDCP wave1 E_ads (box24) | −0.3302 – −0.7728 | eV | `sdcp_wave1_citable.json` | provisional |
| NEB Li 이동 장벽 | Li metal 0.080578 · Li₃Nd 0.228981 · Li₂S 0.305025 · (구경로 Li₃Nd 2.07173) | eV | `sei_neb.json` (roots 5 · 9건) | **전부 `provisional_single_cell` · citable=false · 최상위 `retracted: true`** |
| 표면에너지 γ_SE | 0.45 – 1.211 | J/m² | `adhesion.json` | — |
| C-12 ΔE_ads (SDCP vs PTFE) | **아직 없음** — 외주 16잡 발송 전 | eV | — | 미계산 |

**미세구조·수송 계열**: 이 브랜치에 **없다.** (축 A 는 브랜치 B 에 있다.)

**그 외 내가 발견한 것**: `db/` 아래 `compositions` · `doping` · `interphases` · `spectra` ·
`structures` · `pipelines` · `literature` · `knowledge` 서브트리. `db/properties/` 만 377파일.
oxidation stability cascade(`oxidation_stability_cascade_v3_pinned.json` 등)가 가장 큰 계열인데
이번 조사에서 값 범위까지 파고들지 않았다 — **unknown, 후속 조사 필요.**

---

## 2. 브랜치 B (`claude/stoic-knuth-NObVQ`) 가 본 연구자

> ⚠ **정정 (2026-09-04 2차 조사)** — 1차 보고에서 나는 이 브랜치를 README·main.tex 헤더·CSV 몇 개로만
> 읽고 *"MPM/voxelization 은 1급 코드로 확인되지 않았다(unknown)"* 라고 썼다. **틀렸다.**
> 이 브랜치의 `CLAUDE.md` 는 **2264행짜리 실험노트**이고, MPM 은 FINALIZED 된 production 모델이며
> 최근 90일 커밋 주제 중 **가장 많이 언급된 단어(283회)** 다. 아래가 다시 판 결과다.

### A-1 무엇을 연구하는가
황화물 복합양극을 **DEM(LIGGGHTS)과 MPM(Taichi GPU, J2 소성) 두 개의 독립 모델**로 압밀하고,
각각의 미세구조 위에서 **접촉망 Kirchhoff σ**(Holm 협착)와 **복셀 유한체적 σ**(∇·σ∇φ=0) 라는
**두 개의 독립 수송 해**를 구한다. 거기서 나온 σ_ionic·σ_e·σ_thermal 을 전기화학(비선형 BV +
구형확산 시간전개)까지 밀어 ASR·율특성을 내고, 마지막으로 그 전부를 **물리로 구조화된 회귀**
(스케일링 법칙)로 압축해 설계 수치 → 물성 → 2D 미세구조 합성으로 가는 예측기를 만든다.

**목적 한 줄** (CLAUDE.md "Big goal (user's vision)" 원문):
> *"Given input design numbers → ML predicts the full metric set → draw a 2D microstructure
> matching those numbers → eventually stack different configs as natural LAYERS inside one
> composite cathode."*

**활동**: 2026-03-25 최초 커밋 ~ 2026-09-03 · **커밋 2652개**
(월별 04월 89 · 05월 469 · 06월 744 · 07월 568 · 08월 725 · 09월 56)

### ★ 이 축의 통제 인식론 — frame[4] (FINALIZED 2026-06-07)
CLAUDE.md 가 스스로 *"the controlling epistemology for all compaction/transport work"* 라고 부른다.
> **DEM 과 MPM 을 서로 보정하지 않는다.** 각자 **실험에만** 독립 보정하고 결과를 비교한다.
> 일치 = 교차검증 증거. 불일치 = **정량화된 모형 한계** — 실패가 아니라 정보이고, 둘 다 publishable.
> DEM↔MPM 일치를 강제하는 것(예: MPM σ_y 를 DEM Heckel σ_y_eff 에 맞추기)은 **순환논증**이다.

frame[5] 분업:
- **DEM 고유**: 명시적 접촉망 → **접촉 단위** 협착 저항 · percolation · coverage · force chain ·
  Auerbach 파괴 · **Furnas dip**(MPM 은 어떤 보정으로도 재현 못 함, CORRECTION 2)
- **MPM 고유**: 참 소성 입자 형상 변화 · 부피보존 void-fill 유동 · 공간 누적소성변형/응력장 ·
  입상 스케일 Heckel σ_y_eff
- **둘 다**: 거시 porosity vs (P, 조성, P:S, AM%) · Heckel 선형성 · P_y

⚠ **σ 를 내는 솔버가 둘이고 파이프라인이 다르다** (2026-08-11 사용자 지적으로 발견된 정정):

| | `scripts/network_conductivity.py` | `scripts/voxel_conductivity.py` · `step3_sigma.py` |
|---|---|---|
| 이산화 | DEM 구의 **접촉망** (접촉당 Holm 협착) | MPM **복셀 격자** (유한체적 ∇·σ∇φ=0) |
| 입력 | LIGGGHTS 덤프 | MPM phase grid |
| 실행 위치 | **웹앱 파이프라인** | **MPM 킷** (`run_mpm.sh`) |

한쪽이 다른 쪽의 근사가 **아니다** — 다른 이산화의 독립 측정이고, 그게 frame[4] 교차검증의 상대다.
웹앱 코드리뷰 수정이 STEP3 에 자동 적용되지 않는다(실제로 2026-08-11 에 thermal 무음-결손 결함이
양쪽에 따로 있어 각각 고쳤다).

### A-2 파이프라인 (축 A **내부**에서는 파이프라인이 맞다)
```
STEP1 DEM (LIGGGHTS)  →  STEP2 MPM 압밀/payload  →  STEP3 복셀 σ  →  STEP4 전기화학  →  STEP6 surrogate
  패킹·접촉·force chain    소성 형상·void-fill·응력장   σ_ion/σ_e/k    비선형 BV+구형확산
  Auerbach 파괴            mpm3d_compaction.py        step3_sigma.py  step4_dyn.py
        └───────────── SOC breathing (eigenstrain) → 응력 → 파괴 → 접촉/σ 손실 → 열화 ↺
```
(`pipeline/PIPELINE.md`) LIGGGHTS 로 못 하는 이유가 명시돼 있다 — DEM 비용은 **입자 수**에
비례(나노 카본 = 수백만 객체 = 불가), 격자 비용은 **해상도**에 묶이고 MPM 은 이미 점마다
재료상수(µ, λ, σ_y)를 들고 있어 **첨가제는 "상수가 다른 material point 가 더 있는 것"** 일 뿐이다.

### A-3 산출물 인벤토리
파일 **1841개** · `docs/` 1054 · `scripts/` 490 · `litdb/` 73 · `이종기술/` 45 · `se_curve/` 40 ·
`webapp/` 32 · `wiki/` 31 · `dem_scripts/` 24 · `machine-learning/` 16 · `heckel/` 4 · `pipeline/` 1

| 종류 | 경로 | 무엇 |
|---|---|---|
| **실험노트 정본** | `CLAUDE.md` (**2264행**) | 판정·규약·이력. *"충돌 시 이 파일이 이긴다"* |
| 지도 | `wiki/index.md` (21페이지: concepts·entities·comparisons·guides·questions·syntheses) | 요약+포인터. `wiki/tools/lint.py` |
| **주장 원장** | `docs/reviews/claims.json` | **82건** (live 53 · rejected 20 · hold 5 · retired 4) + **`quotation_ban`** 인용금지 목록 |
| **결함 원장** | `docs/reviews/findings.json` | **123건** (claimed_fixed 93 · open 19 · verified 8 · wontfix 3). `check_review_findings.py` 가 자기일관 강제. `claimed_fixed ≠ verified` |
| 사전등록 | `docs/reviews/*_prereg_*.md` | 런 **전에** 등록한 예측. *"결과 보고 창을 옮기면 무효"* |
| 리뷰 | `docs/reviews/` **113파일** (deep_review 6 · handoff 3 · Codex RC5/RC6 교차 …) | 3각 자체리뷰 + Codex 교차 |
| 세션 기록 | `docs/session_<날짜>_progress.md` | 오늘의 수치·판정 (압축 전 대피소) |
| 원고 | `docs/paper/main.tex` + `refs.bib` | Stage E 논문 (§4 표 참조) |
| 데이터 | `docs/data/` (캠페인별) · `all_dem_porosity.csv` · `validation_all_cases.csv` · `docs/db/section7_10case_sweep.csv` | CSV, 기계 판독 |
| ⚠ 케이스 정본 | `webapp/archive/<campaign>/<case>/full_metrics.json` | *"single source of truth per case"* — **git 추적 0개**, repo 밖 |
| 실험 | `이종기술/eis/` (§축 C) | BioLogic .mpr 원자료 + tidy CSV + catalog + CNLS fits |
| 스킬 | `skills/dem-analysis-{standard,bimodal}.md` | — |

### A-4 살아있는 것 (최근 90일 커밋 주제 빈도)
`mpm 283` · `webapp 95` · `리뷰 91` · `porosity 81` · `sdcp 79` · `step4 73` · `ptfe 68` ·
`eis 68` · `step3 67` · `litdb 61` · `vgcf 55` · `sweep 49` · `voxel 40` · `bimodal 33` ·
`σ_e 32` · `사전등록 27` · `manuscript 27` · `격자 21`

1. **SR-01 격자 수렴 — 미해결이고 원고 헤드라인이 걸려 있다.**
   같은 침대·같은 규약에서 vox 만 0.4 → 0.3 → 0.25 µm 로 조이면 σ_e 비가
   **1.4215 → 1.1621 → 1.0849** 로 내려가고 σ_ion 비는 **부호가 뒤집힌다**(1.0742 → 0.9908).
   더 조여도(0.15 · 0.125 · 0.115) **단조 증가가 멈추지 않고**, 증분비 Δ1/Δ2 = **1.773** 인데
   `R = R∞ − C·h^p` 가 이 간격에서 낼 수 있는 최소가 **2.187**(p→0⁺) ⇒ **어떤 p>0 도 안 맞는다**
   ⇒ **Richardson 외삽 무의미**. 하드웨어 한계 = vox 0.115 µm (실측 peak RSS **35.6 GB**).
   ⇒ *"살아남는 것은 값이 아니라 모양이다"*.
2. **원인 = 표현 부피(representation volume), 실측 확정.** SDCP 표현부피/참부피가
   **4.311(0.4) · 1.866(0.3) · 1.090(0.25) · 0.238(0.15)** = **18.1배 변동**.
   점 스탬프가 섬유를 **20.6–75.8 %** 조각낸다. → `--step3-sdcp-sphere-d`(참 직경 구 스탬프) 신설,
   실침대 부피가 참값의 **0.986배**로 제자리를 찾았다.
3. **인용금지 목록이 운영된다.** 철회된 헤드라인(`+52.0 %` · `+42.15 %` · `f_artifact = 0.147` ·
   `실험의 3.6배` 등)이 `claims.json` 의 `quotation_ban` 에 등재돼 **원고·SI·발표에 쓸 수 없다.**
4. **원고 본문을 DB 로 내리기** (최신 커밋) — 본문 스냅샷 + 판간 diff + 문장별 판정
5. **LHS 스윕** 8개 · **SDCP 전도도 판별 팔**(σ_SDCP = 0) 사전등록 · litdb 흡수 CL-60~65
6. **R_int 풀셀/사이클** Phase 2 (2C DBE R_int={0 ✅ 89.6 %, 10 실행중})

### A-5 확보된 수치 — 미세구조·수송 계열
**형식: CSV(기계 판독) + CLAUDE.md 안의 FINALIZED 절.** ⚠ 케이스별 정본 JSON 은 git 밖이다.

| 물리량 | 범위 | 단위 | 경로 |
|---|---|---|---|
| porosity | 15.0 – 19.7 | % | `section7_10case_sweep.csv` · `all_dem_porosity.csv`(80케이스) |
| percolation | 92.3 – 99.7 | % | 〃 |
| σ_ionic | 0.117 – 0.173 | mS/cm | 〃 |
| σ_electronic | 3.18 – 4.63 | mS/cm | 〃 |
| σ_thermal | 3.42 – 4.33 | mS/cm | 〃 |
| AM–AM CN | 2.73 – 3.86 | — | 〃 |
| SE–SE CN | 4.39 – 5.24 | — | 〃 |
| τ_Laplace | 1.21 – 4.39 | — | 〃 |
| F_DEM (AM_P–AM_P) | 1.32 – 9.04 | mN | 〃 |
| 심각파괴 비율 | 0.0 – 1.23 | % | 〃 |
| porosity 예측 잔차 | −2.91 – +1.52 | %p | `validation_all_cases.csv` |

**보정 상수 (전부 실험 앵커)**
- MPM: **E_eff 1.53 GPa · σ_y 0.15 GPa**(2D). 앵커 = Minnmann pure-SE porosity ≈ **10 % @ 300 MPa** ·
  SEM 유사 core-preserved 형태 · 문헌 σ_y 0.05–0.30 GPa. pure-SE 항복 ≈ 86 %.
- DEM: **E_SE bulk 24 → 유효 1.35 GPa (18× 연화)**. 연화가 뭉뚱그리는 것 = 재배열·GB 미끄러짐·미세파괴.
  앵커 = 300 MPa porosity + pure-SE Cronau overlap 11–12 %.
- Heckel (DEM pure-SE, 4압력): **R² 0.965 · P_y 138 MPa · σ_y_eff 46 MPa**
  (LPSCl 단결정 300 MPa 의 6.5배 연질 — 입상 연화와 정합)
- Furnas dip: AM **75–85 wt%** (Bouvard/McGeary 기하 패킹) — **DEM 전용**
- 2C CCCV (SBE→DBE): delivered CC끝 81.5 → 83.0 (+1.5 %p) · CV후 88.9 → **89.6 %** (+0.7 %p) ·
  CC ΔV **9.3 mV** = 옴 4.5 + kin 4.8 (방전 7.9 mV 와 대칭 = 수송 기원 양방향 확인)

**★ 스케일링 법칙 — 이 축의 헤드라인 산출물 (전부 FINALIZED)**
- **σ_ionic** (2026-05-28) **LOOCV 0.9752** · n=90/k=5 (**18:1**)
  ```
  σ = σ_grain·Cronau(r_SE)·φ_eff^½·CN²·cov_Hertz^½·f_p³
      · exp[a + b·lnτ + c·(lnτ)² + β_P2·P2 + β_F·log f_intact]
  ```
  FROZEN 상수: σ_grain **3.0 mS/cm**(Cronau 2022 LPSCl 단결정) · φc_P **0.200** · φc_S **0.195** ·
  δ **0.040** · r_cut **3.5 µm** · α **2**.
  항별 신뢰도: σ_grain HIGH · Cronau(r_SE) HIGH · φ_eff^½ MED-HIGH · CN² MED-HIGH ·
  cov_Hertz^½ HIGH(Holm 1967, Spearman 0.697 > cov_P 0.476) · f_p³ MED · C(τ) MED(ΔAIC −10.6)
- **σ_electronic** Stage 22.5 (2026-06-03) **LOOCV 0.9531** · R² 0.9613 · **8 LIVE OLS + 2 LOCKED** (9.5:1)
  — Stage 22(12 OLS)에서 전-ablation 스크린으로 약항 4개(β_v·β_AC·β_fpth·β_logrSE)를 **함께 빼니
  LOOCV 가 +0.006 개선**되고 n/k 가 6.3:1 → 9.5:1 로 올랐다 = *"물리적 Lasso"*
- **σ_thermal** Stage T1 (2026-06-04) **LOOCV 0.9028** · R² ≈0.96 · **Ridge α=0.05** · 14 feature (6:1)
  — A/B/C 스크린이 Ridge 가 순수 멱법칙(0.59)·Bruggeman EMT(음수 R²) 대비 불가피함을 확인

`machine-learning/APPLICATION_TO_DEM_DFT.md` 가 이 셋을 강의 이론에 매핑한다 —
*"우리의 transport-triad 스케일링 법칙은 **물리로 구조화된 선형회귀 + 정규화** 그 자체다."*

### A-6 이 브랜치의 방법론적 쟁점 (= 원고 §6 소제목이 곧 목록)
frame[4] 교차보정 금지 · E_SE 18× 연화의 정당화 · **Hooke vs Hertz 등가성** · Auerbach+Lawn 파괴 ·
Stage E grain 보정(Cronau 2021/22 · Trevisanello 2021 · Wang 2022) · high-contrast Laplacian(인자비
20×) → **7층 방어**(adaptive boundary → spsolve sanity → CG retry → ratio guard → §7 이상치 필터 →
**Bruggeman EMT fallback** → …) · SE–SE 입계저항 · **regime 밖 편차를 fit 하지 않는다** ·
준정적 게이트 `V/c_P ≤ 0.01`(위반 = 등급 B, 상대비교 전용) · n/k 비율 규율 ·
*"정보이론적 천장 — 항을 더 넣지 마라"*

## 3. 두 브랜치 종합 (A-6)

| | 브랜치 A `friendly-meitner-lldvar` | 브랜치 B `stoic-knuth-NObVQ` |
|---|---|---|
| 축 | **축 B** (DFT / MLIP) | **축 A** (DEM / MPM / 복셀) + **축 C**(실험 EIS) |
| 커밋 | 최신 2026-09-03 | **2652** (2026-03-25 ~ 2026-09-03) |
| 실험노트 | `kb/` 351문서 + `CLAUDE.md` | `CLAUDE.md` **2264행** + `wiki/` 21페이지 |
| 원장 | `db/governance/decisions.json` (결정 14) · 사전등록 JSON | `claims.json` (주장 82 + 인용금지) · `findings.json` (결함 123) |
| 수치 | `canonical_registry.json` **39항목** (JSON, source_path 결박) | CSV 80+10 케이스 + CLAUDE.md FINALIZED 절 |
| litdb | **정본** (208편) | **동결 스냅샷** (64편, 추가·수정 금지) |
| 웹앱 | 정본값 뷰어 | 케이스 브라우저 + 3D 뷰어 |
| 원고 | AF-ASSB AgNO₃–C–PVP SI 기여 (.docx) | Stage E 저항망 논문 (main.tex, 1저자) |

- **분기점**: **없다.** `git merge-base` rc=1 — 두 개의 독립 루트 커밋. 코드 공유 0.
- **역할 분담**: 완전 분리. 실행 환경도 다르다(축 B = KISTI/kgy/gabia/외주 VASP, 축 A = WSL/V100 킷).
- **겹침 — "번호 하나" 단위 넷.** 자동 연결이 아니라 사람이 값을 옮겨 적는다:
  1. **탄성 상수** — 축 B 의 DFT (E_VRH **22.06 / 27.66 GPa** · B₀ **26.23 GPa** · ν 0.360 · μ 8.11)가
     축 A 의 DEM/MPM 물성 카드에 **인용**돼 있다 (축 A CLAUDE.md L568 · L1131–1141).
     ⚠ 축 A 는 그 값을 **그대로 쓰지 않는다** — DEM 은 E_SE 를 1.35 GPa 로 18× 연화한다.
     DFT 값은 "실-bulk 축" 참조일 뿐이고, 축 A 는 그 차이를 명시적으로 분리해 둔다
     (*"물성 행은 DFT 쌍, ν 0.3 은 DEM 설정에만"*).
  2. **SDCP** — 같은 물질이 양쪽에 있다. 축 B 는 LiNiO₂(104) 위 **흡착에너지**(C-12), 축 A 는 전극 안
     **전도성 첨가제**(σ_SDCP 250 mS/cm). 축 A 의 SDCP 캠페인 문서가 **`잔여 = E_bind DFT(gabia)`** 로
     축 B 의 값을 기다린다 (`[[anchor-waitlist]]` 에 등재).
  3. **litdb** — 정본은 **축 B 브랜치 하나뿐**(2026-07-16 결정). 축 A 것은 동결.
     ⚠ 1차 보고에서 내가 *"중복이라 통합 결정 필요"* 라고 쓴 것은 **틀렸다** — 이미 결정돼 있다.
  4. 공저자용 Methods .docx (v7 / v8) — 같은 원고인지는 unknown.
- **통합 필요 여부**: **아니다.** merge 하면 2652 커밋과 무관 히스토리가 섞이고 얻는 것이 없다.
  litdb 는 이미 단일 서랍으로 정리돼 있다.
- **전체 그림**: 한 사람이 **같은 재료계를 두 스케일에서 따로** 공격한다. 원자 스케일에서는
  "이 값을 인용해도 되는가" 를 절차로 닫고, 입자·연속체 스케일에서는 "이 파이프라인이 언제
  틀리는가" 를 방어층과 격자 수렴으로 닫는다. **공통점은 물리가 아니라 인식론이다** —
  양쪽 다 계산 **전에** 보고량·게이트를 등록하고, 틀린 것을 지우지 않고 원장에 남기며
  (축 A `quotation_ban` · 축 B `retracted`/`superseded`), 외부 적대 리뷰를 돌리고,
  *"확인 못 한 것은 통과가 아니다"* 를 코드가 집행하게 만든다.

## 4. 작성한 research_profile.md 전문

`research-agent/config/research_profile.md` · `status: FILLED (by Claude Code, 2026-09-04)`

```markdown
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

### 대상 조성·계면
- **Li₆PS₅Cl 계열**: comp1–comp5 · `modelc`(=LPSCl1.6) · +B₂O₃ · LPSOCl(+O) · Nd 치환
- **계면**: LiNiO₂(104) 슬랩 192원자 × 바인더 조각 — **SDCP(설폰화 전도성 고분자) vs PTFE(C10)**
  (자기 seed 2종 `afm2424_pm1` / `afm2424_net4`, U(Ni d)=6.2, D3 zero-damping)
- **SEI 분해상**: Li metal(bcc) · Li₂S · Li₃N–Nd · Li₂O · Li₃P · Li₃PO₄(β/γ) · LiCl · LiNdO₂ · Nd₂O₃ · Nd₂S₃
- **AF-ASSB 원고**: Li₃N(001) · LiC₆(0001) 표면
- **Zn ALZIB (C1)**: Cu–Zn 상 지문 — 43°±1° 에 8상이 1.47° 폭으로 겹침, Cu–Zn 간격 0.097°

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
| NEB Li 이동장벽 | Li metal **0.0806** · LiNdO₂ **0.229** · Li₂S **0.305** eV | **전부 `provisional_single_cell` · citable=false** |
| 표면에너지 γ_SE | 0.45 – 1.211 J/m² | — |
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
- 액체·폴리머 전해질 전용 · Li–S(황화물 SE 아님) · Zn/Na/K 이온
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
```

---

## 5. 수치 인벤토리 (요약)

| 계열 | 브랜치 | 형식 | 기계 판독 | 경로 | 항목 수 |
|---|---|---|---|---|---|
| 원자 스케일 (gap · B₀ · 탄성 · MD Ea · ICOHP · E_ads · NEB) | A | JSON | ✅ (registry 가 원자료를 가리킴) | `db/properties/canonical_registry.json` + 377 파일 | 정본 39 |
| 미세구조·수송 (porosity · σ · percolation · CN · τ · 접촉력) | B | CSV | ✅ | `docs/db/section7_10case_sweep.csv` · `all_dem_porosity.csv` · `validation_all_cases.csv` | 80 + 10 케이스 |
| 케이스별 정본 | B | JSON | ✅ 이지만 **git 밖** | `webapp/archive/<campaign>/<case>/full_metrics.json` | git 추적 0 |
| 문헌 수치 | A · B | Markdown 표 (digest §3) | ❌ **비구조화** | `litdb/papers/*.md` | 272 digest |

**가장 중요한 구조적 사실**: 내 결과는 기계 판독 가능한데 **문헌 수치는 Markdown 표 안에 있다.**
C-1(수치DB)이 노리는 지점이 정확히 여기다.

---

## 6. 설치 결과 (B-1)

```
$ cd research-agent && pip install -e ".[dev,llm]"
Successfully built research-agent
Successfully installed annotated-types-0.8.0 anthropic-1.3.0 anyio-4.15.0 beautifulsoup4-4.15.0
docstring-parser-0.18.0 h11-0.16.0 httpcore2-2.12.0 httpx2-2.12.0 idna-3.19 iniconfig-2.3.0
jiter-0.16.0 lxml-6.1.3 markdown-3.10.3 pluggy-1.6.0 pydantic-2.13.5 pydantic-core-2.46.5
pygments-2.21.0 pytest-9.1.1 research-agent-0.1.2.dev0 sniffio-1.3.1 soupsieve-2.9.2
truststore-0.10.4 typing-inspection-0.4.4

$ python -m pytest -q
........                                                                 [100%]
8 passed in 0.25s

$ ra status
research-agent v0.1.2.dev0 · root=/home/user/Yonghoon-DEM-DFT/research-agent
papers: {'digested': 5, 'rejected': 1, 'total': 6}
analysis queue (pending): 0
last digest: 2026-09-04 (sent_at=2026-09-03T16:04:23+00:00)
  run#1 morning ok 2026-09-03T16:04:23+00:00 → 2026-09-03T16:04:23+00:00 {"date": "2026-09-04", "sent": true, "via": "cowork-gmail-mcp", "n_papers": 5, "n_a": 4, "n_b": 1, "n_c": 0, "db_total": 6, "n_week": 6, "n_rejected": 1}
  [A] IF 48.5 rel 0.55 digested  Planar Li deposition and dissolution enable practical anode-free pouch
  [A] IF 26.8 rel 0.6 digested  Revealing the Neglected Role of Passivation Layers of Current Collecto
  [A] IF 15.7 rel 0.95 digested  Using resistor network models to predict the transport properties of s
  [A] IF 15.7 rel 0.9 digested  Mechanofusion-derived cathode composite microstructures with scalable
  [B] IF 15.7 rel 0.45 digested  Domain oriented universal machine learning potential enables fast expl

$ ra morning --dry-run
[ra 23:31:21] git commit: ra: morning 2026-09-04 (+0 papers, 0 analyzed)
[ra 23:31:21] morning done: 2026-09-04 {'n_papers': 0, 'n_a': 0, 'n_b': 0, 'n_c': 0, 'db_total': 6, 'n_week': 6, 'n_rejected': 1} sent=False
```

병합: `claude-code/CLAUDE.md` → repo 루트 `CLAUDE.md` 끝에 `## research-agent` 절로 추가 (기존 전문 유지).
복사: `.claude/commands/paper-{morning,noon,sync}.md` · `.claude/agents/paper-analyst.md` → 루트 `.claude/`.
커밋: `ffa0e8546 research-agent 설치 + research_profile 작성`.

---

## 7. litdb (B-2)

**결론: SQLite 도 .bib 도 Zotero 도 papers.json 도 아니다. Markdown digest 체계다.**

| | 브랜치 A | 브랜치 B |
|---|---|---|
| 경로 | `litdb/papers/*.md` | `litdb/papers/*.md` |
| 레코드 수 | **208** (DOI 있는 것 199) | **64** (DOI 있는 것 61) |
| primary key | 파일 stem = `slug` (예: `duquesnoy2020_calendering_ml_mesostructure_generator`) | 동일 |
| 인덱스 | `INDEX.md` · `INDEX_DEM.md` · `INDEX_DEM_snapshot_2026-07-16.md` | `INDEX.md` · `NOVELTY.md` · `WISHLIST.md` |
| 부가 | `topics.json` · `pdf_map.tsv` · `figures/_sources.json` · `our_dft_baseline.md` · `comparison_vs_ours.md` · `comparison_vs_ours_DEM.md` | `our_dem_baseline.md` · `comparison_vs_ours.md` · `contact_models_layer_map.md` |
| 읽고 쓰는 코드 | `.claude/agents/litdb-curator.md` (서브에이전트) · `tools/litdb/extract_figures.py` | `skills/` |

**고유 DOI 195개** → `research-agent/data/known_dois.txt` (형식: `브랜치<TAB>slug<TAB>DOI`).
DOI 없는 digest 12건은 `UNKNOWN` 으로 표기.

★★ **정정 — 어느 쪽이 정본인지 이미 정해져 있다** (1차 보고에서 "통합 결정 필요" 라고 쓴 것은 틀렸다).
`claude/friendly-meitner-lldvar` 의 `litdb/` 가 **유일한 정본**이고, `stoic-knuth` 의 `litdb/` 는
**2026-07-16자 동결 스냅샷**(참조 가능, 추가·수정 금지)이다. 기존 63장은 정본으로 이관 완료.
어느 세션에서 일하든 새 카드는 정본 브랜치에만 넣는다 (litdb 한정 그 브랜치 커밋/푸시 상시 승인).
근거: 축 A `CLAUDE.md` §"litdb 정본(단일 서랍) 규칙" · `wiki/entities/litdb-canon.md`.

⛔ **중복 확인을 INDEX 로 하면 안 된다 — 인덱스가 셋이다** (2026-09-03 실측 사고, 축 A CLAUDE.md 기록).
정본에는 `INDEX.md`(argyrodite SE 축) · `INDEX_DEM.md`(DEM·건식전극 축) ·
`INDEX_DEM_snapshot_2026-07-16.md`(동결) 이 있다. `INDEX.md` 만 grep 하고 "없다" 고 판정해
**이미 526줄 2판까지 있던 카드**를 새로 만들 뻔했다 (2026 ECER 중복 사고와 같은 구조).
⇒ 안전한 확인은 **파일 목록 자체**를 보는 것:
```
git ls-tree FETCH_HEAD litdb/papers/ --name-only      # 전수
git grep -i '<DOI 또는 제목 낱말>' FETCH_HEAD -- litdb/  # 인덱스 무관
```
⇒ **에이전트에게도 "INDEX 를 보라" 가 아니라 "papers/ 를 보라" 로 지시해야 한다.**
(내가 만든 `known_dois.txt` 는 papers/ 전수에서 뽑았으므로 이 규칙에 맞다.)

**레코드 1건 전문** — `litdb/papers/_TEMPLATE.md` (필드명 전체가 여기 있다):
```
<!-- digest 표준 양식. 복사해서 papers/<slug>.md 로. ★ = 사용자가 특히 원한 항목 -->
# <제목> — <제1저자> (<저널> <년>)

> slug `<slug>` · DOI `<doi>` · type `exp|DFT|AIMD|MLIP|mixed` · PDF `<upload-id>.pdf` · digested `<날짜>` · status ✅

## 1. 한 줄 요약
## 2. 메타        | 저자 | 저널/년 | DOI | 조성 | 연구유형 |
## 3. 핵심 물성 (수치)  | 물성 | 값 | 조건 | 비고 |
      이온전도도 σ / 활성화E Ea / 산화 onset·ESW / 기계적(E,B,G,C_ij) / 전자구조(gap, VBM/CBM)
## 4. DFT/계산 방법 ★  code·version / functional+vdW / pseudo·PAW / k-points·ecut·supercell·nat /
      DFT+U / AIMD(ensemble,T,time,thermostat) / MLIP(model, training set) / 무질서 처리 / 특이사항
## 5. Figure set ★     | Fig | 내용 | 우리가 참고할 점 |
## 6. Post-processing ★ 무엇(BVSE/NEB/Bader/COHP-ICOHP/DOS-PDOS/ESW/ELF) / 도구 / 수치화·플롯·기록 방식
## 7. 우리 DFT 대비 (comp1 / modelc) → our_dft_baseline.md
```

⚠ **`.sqlite` 는 딱 하나 있다** — `research-agent/data/papers.sqlite` (에이전트가 방금 만든 자기 DB,
6 레코드). 사용자의 litdb 와 **무관**하다. `.bib` 도 하나 — `docs/paper/refs.bib` (브랜치 B 원고 참고문헌).

**치명적 부정합**: `research_agent/exporters/litdb.py` 는 어댑터가 **둘뿐**이다 —
`cli`(John Kitchin litdb, PATH 에 없음) 와 `file`(JSONL 또는 SQLite). **Markdown digest 어댑터가 없다.**
지금 `ra litdb` 를 돌리면 실제 litdb 와 **영영 합쳐지지 않는 평행 JSONL** 이 생긴다.

---

## 8. vault (B-3)

**절대 경로**: `/home/user/Yonghoon-DEM-DFT/research-agent/vault`
**repo 밖 Obsidian vault 는 없다** (`find / -maxdepth 5 -type d -name '*vault*'` → 0건).
⚠ 단, 여기는 **클라우드 컨테이너**다. 사용자의 실제 Obsidian vault 는 로컬/데스크톱에 있을 수 있다 — **unknown.**

```
vault/
├── 00_MOC/Research Agent Home.md
├── Papers/2026/  (3) · 2025/  (2)
├── Keywords/  dem battery.md · dft battery.md · anode-less assb.md
├── Digests/2026-09-04.md
└── Templates/  paper_note.md · daily_digest.md
```

**파일명 규칙**: `Papers/<year>/<year> - <FirstAuthorLastName> - <제목 앞부분>.md`
예: `2025 - Ketter - Using resistor network models to predict the transport.md`

**frontmatter 전문** (실제 노트에서):
```yaml
---
title: "Using resistor network models to predict the transport properties of solid-state battery composites"
aliases: ["Using resistor network models to predict the transport"]
authors: ["Lukas Ketter", "Niklas Greb", "Tim Bernges", "Wolfgang G. Zeier"]
journal: "Nature Communications"
year: 2025
doi: "10.1038/s41467-025-56514-5"
url: "https://www.nature.com/articles/s41467-025-56514-5"
if: 15.7
tier: "A"
relevance: 0.95
status: digested
keywords: ["dem battery"]
tags: ["paper/dem", "tier/A", "topic/resistor-network", "topic/effective-conductivity", "material/LPSCl", "material/NCM83"]
source: bootstrap
date_added: 2026-09-03
analyzed_at: 2026-09-03
evidence_level: fulltext
ra_id: "doi:10.1038/s41467-025-56514-5"
---
```

**태그 상위** (노트 5건 기준이라 통계가 안 된다 — 관찰된 것 전부):
`paper/dem` · `paper/dft` · `tier/A` · `tier/B` · `topic/resistor-network` · `topic/effective-conductivity` ·
`topic/anode-free` · `material/LPSCl` · `material/NCM83` — **상위 20개를 낼 표본이 없다.**

**Dataview**: 쓰지 않는다. `prompts/style_guide.md:22` — *"Dataview 인라인 필드는 frontmatter로 대체(중복 금지)."*

**연결 방법 제안 (실행 안 함)**:
1. `config/agent.yaml` 의 vault 경로를 사용자의 실제 Obsidian vault 로 지정 (경로 확인 필요 — unknown)
2. 지금 vault 는 research-agent 전용 하위 폴더로 두고, 실제 vault 에서 **symlink** 로 `Papers/` 만
   노출 — 폴더 구조를 안 바꾸면서 Obsidian 이 읽게 하는 최소 개입
3. `tags` 에 `paper/dem` / `paper/dft` 를 이미 축별로 붙이고 있으므로, 실제 vault 의 기존 태그 체계와
   충돌하는지 **먼저 확인해야 한다** (기존 vault 를 못 봐서 판단 불가)

---

## 9. 환경 (B-4)

⚠ **여기는 사용자의 24시간 가동 기계가 아니라 Claude Code 클라우드 컨테이너다.** 아래는 이 컨테이너 값이다.

| 항목 | 값 |
|---|---|
| OS | Linux vm 6.18.44-fc-v24 x86_64 |
| Python | 3.11.15 |
| 24시간 가동 | **아니다** — 세션 종료 시 컨테이너 회수 |
| `which claude` | `/opt/node22/bin/claude` |
| `which hermes` | **없음** |
| `which litdb` | **없음** (→ `exporters/litdb.py` 의 `cli` 어댑터 사용 불가) |
| `ANTHROPIC_API_KEY` | **unset** |
| 교내망 전문 접근 | **없음** (프록시 경유 클라우드) |
| crontab | **명령 자체가 없음** · systemd/launchd 미확인 |
| git remote | `origin https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT` (fetch/push) |
| push 권한 | 있음 (이 세션에서 실제 push 성공) |

**사용자의 실제 계산 기계** (`CLAUDE.md` 근거, 이 컨테이너 아님):
- **KISTI** neuron (Slurm, QOS 제출 제한)
- **kgy** RTX3090 · QE-GPU + uma env · `ssh kgy@59.12.161.91`
- **gabia** A6000 단일 GPU · QE-GPU + fairchem/UMA · `root@121.78.116.27` (pw.x 와 UMA 동시 실행 금지)
- **desktop WSL** — ORCA r2SCAN-3c

→ **research-agent 를 24시간 돌릴 자리는 이 셋 중 하나여야 한다.** 어디에 둘지 **결정이 필요하다.**

---

## 10. 점검 (B-5)

### 어색한 한국어 3개 (실제 생성물에서 인용)
`research_agent/digest.py:105-107` 이 만든 `vault/Digests/2026-09-04.md`:

1. **`"오늘은 총 0편이고 키워드별로는 -입니다."`**
   키워드가 없을 때 `kw_str` 이 `-` 라서 문장이 깨진다. 0편이면 이 절을 통째로 빼야 한다.
2. **`"안녕하세요 용훈님, 2026-09-04 디제스트예요."` → `"... 새로 분석된 논문이 없어요."`**
   `style_guide.md:26` 은 *"첫 두 줄은 해요체 인사 + 오늘 요약 한 문장. 본문은 평서체"* 인데,
   같은 두 문장 안에서 **해요체(`디제스트예요`·`없어요`)와 합쇼체(`-입니다`)가 섞였다.**
3. **`"오늘은 총 0편이고 ... 새로 분석된 논문이 없어요."`** — 같은 사실을 두 번 말한다. 중복이다.

### 코드 버그
1. **`research_agent/cli.py:368`** — `ra morning --dry-run` 이 **git commit 을 한다.**
   `dry_run` 은 `:365` 의 `_send_digest` 만 막고, `:368` 의 `_git_commit` 은 게이트 밖이다.
   실측: 커밋 `f162397a6 ra: morning 2026-09-04` 가 내 브랜치에 생겼다 (14파일 · sqlite 포함).
   `ra noon` 의 `:351` 도 같은 구조인데 그쪽은 `dry_run` 게이트가 **아예 없다.**
2. **`research_agent/exporters/litdb.py`** — `file` 어댑터가 JSONL/SQLite 만 지원한다.
   사용자의 litdb 는 **Markdown digest** 라 `field_map` 을 아무리 맞춰도 쓸 수 없다 (§7).
3. **`research_agent/digest.py:106`** — `kw_str` 이 빈 값일 때의 분기가 없다 (위 어색한 한국어 #1의 원인).

### triage.py `_TERMS` — A 에서 정의한 프로필에 비추어
**빠진 것** (프로필의 축 핵심어인데 `_TERMS` 에 없다):
- 축 A: `MPM`, `material point method`, `voxel`, `Kirchhoff`, `Bruggeman`, `constriction resistance`,
  `effective medium`, `Heckel`, `coordination number`, `ASR`, `area specific resistance`
- 축 B: `NEB`, `nudged elastic band`, `COHP`, `ICOHP`, `LOBSTER`, `bond valence`, `BVSE`,
  `band gap`, `VASP`, `Quantum ESPRESSO`, `binder`, `PTFE`, `PVDF`
- 시스템: `NCM811`, `NMC811` (`\bNCM\b` 만 있어 `NCM811` 은 단어경계 때문에 **안 잡힌다**)

**잘못된 것**:
- `_TERMS[0]` 이 축 A 와 축 B 핵심어를 **한 그룹(0.35)** 에 묶었다. 프로필은 "한 축만 맞아도 높은
  점수" 라고 하는데, 지금 구조는 두 축 용어가 같이 나오면 diminishing-returns 로 **더 높은 점수**를
  준다 — 억지로 두 축을 잇는 논문을 우대하는 방향이다. 축별로 그룹을 갈라야 한다.
- 감점 목록에 `CALPHAD`, `battery management`, `state of charge estimation` 이 없다 (프로필에 추가함).
- `solid electrolyte(?!\s+interphase)` 로 SEI 를 제외하는데, 축 B 는 **SEI 상의 NEB 장벽이 실제
  연구 대상**이다 (`sei_neb.json`). 이 negative lookahead 는 축 B 에 손해다.

---

## 11. 기능 7개 평가 (C)

| # | 기능 | 필요도 | 난이도 | 기존과 겹침 | 어떻게 붙일까 |
|---|---|---|---|---|---|
| 1 | 수치DB | **5** | 3 | `litdb/papers/*.md` §3 표 · `comparison_vs_ours*.md` (수동) | digest §3 표 파서 + `db/properties/canonical_registry.json` 과 같은 스키마 |
| 2 | 선점 경보 | **5** | 2 | 없음 | `research_profile.md` 의 "진행 중" 절을 기계 판독 가능하게 |
| 3 | 피드백 루프 | 2 | 3 | 없음 | vault frontmatter 에 `read_status` 추가 |
| 4 | 역방향 질의 | 4 | 2 | `comparison_vs_ours.md` (수동) | #1 의 DB 에 질의 |
| 5 | 그룹 추적 | 3 | 2 | `litdb/yonsei_dtbl_lab_triage_2026.md` | bib·digest 저자 집계 |
| 6 | 월간 종합 | 3 | 2 | `kb/seminars/` | 기존 세미나 형식 따르기 |
| 7 | 세미나 지원 | 4 | 2 | `kb/papers/lpscl_vs_lpscl16_seminar_*.md` (형식 있음) | 그 형식·문체를 그대로 |

### 1. 수치DB — **필요도 5. 가장 값어치 있다.**
§5 의 구조적 사실이 근거다: **내 결과는 이미 기계 판독 가능한데(JSON/CSV) 문헌 수치만 Markdown
표 안에 갇혀 있다.** 272개 digest 의 `## 3. 핵심 물성 (수치)` 표는 **이미 `물성|값|조건|비고`
4열로 표준화돼 있다** — 파서를 쓸 수 있다.

A-5 의 내 데이터와 같은 축에 놓을 수 있나: **축 B 는 놓을 수 있고, 축 A 는 조건부다.**
- 축 B: digest §3 의 `이온전도도 σ` `활성화E Ea` `산화 onset/ESW` `기계적(E/B/G)` `전자구조(gap)`
  가 `canonical_registry` 의 `comparison_group` 과 거의 1:1 대응한다.
- 축 A: porosity·σ_eff·τ 는 **압축압력·입경분포에 강하게 의존**해서 조건 없이 나란히 놓으면
  안 된다. `condition` 필드가 필수다.

제안 스키마 (`canonical_registry.json` 의 `comparison_group` 규율을 그대로 가져온다):
```json
{"quantity": "sigma_ionic", "value": 1.3, "unit": "mS/cm",
 "condition": {"T_K": 298, "phase": "Li6PS5Cl", "method": "EIS", "density_pct": 95},
 "system": "Li6PS5Cl", "doi": "10.1038/...", "source": "litdb/papers/<slug>.md#3",
 "comparison_group": "sigma-ionic-RT-EIS-pellet",   // ★ 이게 없으면 섞인다
 "confidence": "table|figure-read|text"}            // ★ figure-read 를 구분 (CLAUDE.md 규율)
```
⚠ **`comparison_group` 없이 만들면 안 된다.** `canonical_registry.json` 의 `_rules` 가 이미
*"comparison_group 이 같은 값끼리만 순위·비교·레이더에 함께 올린다. 프로토콜이 다르면 group 도
다르다"* 고 못박고 있다. 문헌 수치는 프로토콜이 제각각이라 이 규율이 더 중요하다.

### 2. 선점 경보 — **필요도 5. 난이도가 제일 낮은데 효과가 크다.**
근거: 축 A 는 원고가 초안 전 섹션 상태이고(`main.tex` 1034행+), 축 B 는 C-12 가 아직 발송도 안 됐다.
**둘 다 선점당하면 치명적인 시점**이다. 실제로 브랜치 B 는 이미 그 상황을 겪었다 — 커밋
*"Duquesnoy 2020 (ref 67) 흡수 — 그들 ML 타깃 하나가 항등식이다, 우리가 닫은 그 함정"*.

A-4 를 어떻게 기술해야 판정되나 — `research_profile.md` 에 기계 판독 가능한 절을 하나 더 둔다:
```yaml
active_claims:
  - id: stageE-porosity-prediction
    axis: A
    claim: "physics-first porosity prediction without out-of-regime fitting, 80-case validated"
    alert_if: ["porosity prediction", "DEM compaction", "packing density model", "Heckel"]
    stage: manuscript-draft        # 선점당하면 손실이 큰 순서
  - id: c12-binder-contrast
    axis: B
    claim: "DFT adsorption-energy contrast between SDCP and PTFE binder fragments on LiNiO2(104)"
    alert_if: ["binder adsorption", "PTFE cathode interface", "polymer binder DFT"]
    stage: not-yet-computed        # ★ 제일 위험
```
`alert_if` 가 걸리면 tier 가 아니라 **경보**로 올린다. 판정은 LLM 이 아니라 **정규식 먼저** —
오탐이 나도 경보는 놓치는 것보다 낫다.

### 3. 피드백 루프 — **필요도 2. 지금은 표본이 없다.**
vault 노트가 5건이다. 읽음/유용함 신호를 모으려면 최소 수십 건이 필요하고, 그전에는 잡음만 학습한다.
구조상 읽는 법: frontmatter 에 `read_status: unread|read|useful|ignored` 를 추가하고
`ra vault` 가 **덮어쓰지 않게** 보존 로직을 넣는 것 (지금은 재생성이라 손으로 쓴 값이 날아간다 — 확인 필요).
**3개월 뒤로 미루자.**

### 4. 역방향 질의 — **필요도 4. #1 이 되면 거의 공짜다.**
어디에: **litdb 도 vault 도 아니고 #1 의 수치DB 다.** litdb digest 는 사람이 읽는 문서고 vault 는
Obsidian 표시층이다. 질의는 구조화된 DB 에 해야 한다. 다만 답에는 **digest 경로를 같이 돌려줘야**
사람이 원문을 확인한다 (`source` 필드).

### 5. 그룹 추적 — **필요도 3. 근거 있는 목록을 낼 수 있다.**
지금 repo 로 확인되는 것 (digest·bib 기준, **이번 조사에서 저자 집계는 안 돌렸다 — 목록화는 후속**):
- **Zeier (Münster)** — `2025 - Ketter - Using resistor network models...` (relevance 0.95, 축 A 최직접 선행)
- **Cronau · Trevisanello · Wang** — Stage E grain 보정 세 인자의 출처 (원고 §3)
- **Duquesnoy (Franco 그룹, Amiens)** — calendering ML voxel 생성기, CL-65 로 흡수
- **Lawn · Auerbach · Holm** — 파괴·접촉저항 이론 근거
- **Bielefeld · Ngandjong** — 복합양극 미세구조 모델링
축 B 쪽 그룹은 이번 조사에서 **확인 못 했다 (unknown)** — `litdb/INDEX.md` 208편 저자 집계가 필요하다.

### 6. 월간 종합 — **필요도 3.**
`kb/seminars/` 에 이미 형식이 있다. 새 형식을 만들지 말고 그걸 따라야 한다.
그룹미팅 주기를 모른다 (unknown) — 월간이 맞는 주기인지 확인 필요.

### 7. 세미나 지원 — **필요도 4. 기존 형식이 이미 있다.**
따라야 할 형식 (반드시 이걸 쓸 것, 새로 만들지 말 것):
- `kb/papers/lpscl_vs_lpscl16_seminar_script_outline.md` — 개요
- `kb/papers/lpscl_vs_lpscl16_20min_script.md` — **20분 한국어 스크립트**
- `kb/papers/lpscl_vs_lpscl16_seminar_v1.pptx` + `kb/seminars/generate_draft27_claude.js` — 슬라이드 생성
- `litdb/papers/*__seminar_5min_qa.md` — **5분 Q&A 형식 digest 가 이미 3건 있다**
  (`deng2026_...` · `kim2025_...` · `tu2026_...`) ← 이게 정확히 기능 7 이 만들려는 것이다.
  **이미 형식이 있으니 그 형식으로 자동 생성하면 된다.**
⚠ `kb_wiki lint` 가 *"litdb INDEX*.md 어디에도 없는 digest 3개"* 로 이 세 파일을 잡고 있다 —
인덱스 등록이 빠져 있다. 기능 7 을 붙일 때 같이 고쳐야 한다.

### C-8 내 제안 — repo 를 본 사람으로서 더 시급한 것

**8-1. litdb Markdown 어댑터 (필요도 5, 난이도 2) — 이게 1순위다.**
§7 의 부정합이다. 지금 `ra litdb` 는 실제 litdb 와 **영영 안 합쳐지는 평행 JSONL** 을 만든다.
`exporters/litdb.py` 에 `markdown` 모드를 추가해 `litdb/papers/<slug>.md` 를 `_TEMPLATE.md` 형식으로
쓰고 `INDEX.md` 에 등록해야 한다. **이걸 안 하면 나머지 기능이 전부 사용자 자산과 분리된다.**
slug 규칙은 기존 208편에서 추출 가능하다 (`<firstauthor><year>_<topic_snake>`).

**8-2. 중복 판정을 인덱스 3개에 대해 하기 (필요도 4, 난이도 1).**
브랜치 B 커밋이 *"내 중복 확인 방법이 틀렸다 — litdb 인덱스가 셋이다"* 라고 스스로 적었다.
`known_dois.txt` 를 만들어 뒀으니(195 DOI) `triage` 가 그걸 먼저 보게 하면 된다.
**이미 읽은 논문을 다시 올리는 것이 신뢰를 제일 빨리 깎는다.**

**8-3. 축 오분류 감시 (필요도 4, 난이도 1).**
`_TERMS` 가 두 축을 한 그룹에 묶고 있어서(§10) 축 판정이 안 된다. digest·노트에 `axis: A|B|both|none`
를 명시하고, **월 1회 오분류율을 자기보고**하게 한다. 프로필의 "무관한 논문의 특징" 이 그 판정 기준이다.

### C-9 반대 의견 — 하지 말아야 할 것

1. **Scholar alert 를 자동 등록하지 마라.** 지시에도 금지돼 있지만 이유를 덧붙인다 — 키워드가
   `dem battery`/`dft battery` 두 개뿐인데 축 B 의 실제 관심사(NEB·ICOHP·바인더 흡착)는 그 키워드로
   안 잡힌다. **키워드를 늘리기 전에 §10 의 `_TERMS` 부터 고쳐야** 오탐만 늘지 않는다.
2. **두 브랜치를 merge 하지 마라.** 공통 조상이 없어서 merge 하면 2652 커밋과 무관 히스토리가
   섞인다. 얻는 것은 litdb 통합 하나뿐인데, 그건 파일 복사로 된다.
3. **LLM 관련도 점수를 규칙 점수보다 우선하지 마라.** 이 연구자의 작업 방식은 "확인 못 한 것은
   통과가 아니다" 다 (`db/properties/sdcp_c12_claim_prereg_2026_08_31.json` 50행). 설명 없는 LLM
   점수는 그 규율과 정면으로 어긋난다. `rule_relevance` 의 `hits` 를 항상 같이 보여야 한다.
4. **vault 를 재생성으로 덮어쓰지 마라.** 사용자가 손으로 쓴 메모가 날아간다. 기능 3 이전에
   보존 로직부터 확인해야 한다.
5. **문헌 수치를 우리 db 에 직접 넣지 마라.** `CLAUDE.md` — *"문헌 수치는 소환값 — 우리 db 절대값과
   섞지 않기 (방법 명시 없이 이식 금지)."* 수치DB(#1)는 반드시 **별도 파일**이어야 한다.
6. **`ra morning` 을 24시간 기계에 걸기 전에 `--dry-run` 커밋 버그(§10)부터 고쳐라.**
   지금 상태로 cron 에 걸면 매일 무의미한 커밋이 쌓인다.

---

## 12. 추가 제안 (= C-8, 위 참조)

## 13. 하지 말 것 (= C-9, 위 참조)

---

## 14. 결론

안용훈은 **같은 재료계(황화물 ASSB)를 두 스케일에서 따로 공격하는 사람**이고, 그 둘을 잇는 것은
파이프라인이 아니라 **인식론**이다.

`claude/stoic-knuth-NObVQ`(축 A·C, 2652커밋)에서는 DEM(LIGGGHTS)과 MPM(Taichi J2)을 **서로 보정하지
않고 각자 실험에만 보정해** 압밀 미세구조를 만들고, 접촉망 Kirchhoff σ 와 복셀 유한체적 σ 라는
**두 개의 독립 수송 해**를 구한 뒤 전기화학까지 밀어, 마지막에 그 전부를 LOOCV 0.90–0.98 의
**물리로 구조화된 스케일링 법칙 셋**으로 압축한다. 목표는 *"설계 수치 → ML 이 전 물성 예측 →
그 수치에 맞는 2D 미세구조를 그리고 → 서로 다른 구성을 한 복합양극 안의 층으로 쌓기"* 다.
여기에 한양대 이종원 그룹과의 **실제 EIS 측정**(BioLogic VSP-300, 소립 4 µm single-crystal NCM)이
STEP4 의 R_int 앵커로 붙는다.

`claude/friendly-meitner-lldvar`(축 B)에서는 VASP·QE·UMA·ORCA 로 밴드갭·탄성·ICOHP·NEB 장벽·
바인더 흡착을 내되, **계산 전에 보고량을 정의하고 사전등록하고 게이트를 박는다.** 채택 배경이
이 축의 성격을 그대로 말한다 — SDCP 흡착에너지를 여덟 번 계산하고 여덟 번 반려됐는데, 받은
리뷰는 전부 "제대로 돌렸나" 였고 전부 통과했으며 "맞는 양을 재고 있나" 는 여덟 번째에야 물었다.

두 브랜치는 **git 공통 조상이 없고**(rc=1) 코드를 공유하지 않는다. 접점은 넷이고 전부 **"번호
하나" 단위**다 — 축 B 의 탄성 상수가 축 A 물성 카드에 인용되고(그마저 축 A 는 18× 연화해서 쓴다),
**SDCP** 라는 같은 물질을 양쪽이 다른 스케일에서 다루며 축 A 가 축 B 의 `E_bind` 를 **앵커 대기
큐에서 기다리고 있고**, litdb 정본은 축 B 브랜치 하나이며, 공저자용 Methods 를 각각 낸다.
한쪽 출력이 다른 쪽 입력으로 흘러가지 않는다. **"DFT→MLIP→DEM→FEM 다중스케일 파이프라인" 은
틀렸다** — 정확히는 **두 개의 독립 연구 프로그램이 재료와 문헌 서랍을 공유한다.**

⚠ **1차 보고의 오류를 여기 남긴다.** 나는 처음에 축 A 를 README·main.tex 헤더·CSV 몇 개로만 읽고
*"MPM/voxelization 은 1급 코드로 확인되지 않았다(unknown)"* 라고 썼다. 실제로는 MPM 이 FINALIZED
production 모델이고 최근 90일 커밋에서 **가장 많이 언급된 주제(283회)** 이며, 복셀화는 STEP3 의
본체다. 2264행짜리 `CLAUDE.md` 를 안 읽은 것이 원인이다. Cowork 는 **이 문서의 2차 판정을
쓰고 1차 판정을 버려야 한다.**

따라서 research-agent 가 이 사람에게 쓸모 있으려면, 논문을 많이 물어오는 것이 아니라 —
**이미 읽은 것을 다시 올리지 않고**(§10 known_dois, papers/ 전수 확인), **사용자의 실제 litdb
정본에 쓰고**(§C-8-1 Markdown 어댑터), **세 축을 갈라서 채점하며**(§10 `_TERMS` 가 지금은 두 축을
한 그룹에 묶어 억지 연결을 우대한다), **진행 중인 주장이 선점당할 때 경보를 울려야** 한다
(축 A 는 원고 초안이 완성 단계이고 축 B 는 C-12 가 아직 발송 전이라 둘 다 지금이 제일 위험하다).
그리고 이 사람의 규율상 — **설명 없는 LLM 점수는 이 프로필과 정면으로 어긋난다.**
`rule_relevance` 의 hits 를 항상 같이 보여야 한다.

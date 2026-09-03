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

### A-1 무엇을 연구하는가
LIGGGHTS 로 황화물 복합양극을 **준정적 압축**해 만든 입자 패킹에서 접촉망을 뽑아, **Kirchhoff
저항망**으로 이온·전자·열 세 채널을 동시에 풀고, 접촉별 **파괴 분류(Lawn/Auerbach)** 와 문헌 기반
**grain 보정(Stage E)** 을 걸어 셀 레벨 **ASR** 까지 간다. 그리고 그 파이프라인이 언제 못 믿을
값을 내는지를 **7층 방어와 자기보고 카드**로 스스로 신고하게 만든다.

근거:
- `docs/paper/main.tex` — 제목: *"Stage E fracture-aware network solver for all-solid-state battery
  cathode microstructure: a literature-grounded multi-physics framework with 7-layer defence and
  Bruggeman fallback"*, 저자 필드 `Yonghoon Kim`, 소속 KAIST
  ⚠ **저자명이 "Kim" 으로 적혀 있다.** 사용자는 안용훈이다. 오기인지 다른 사람인지 **unknown** — 확인 필요.
- `README.md` — 파이프라인 도식 (LIGGGHTS → network_conductivity.py → run_network_full_corrections.py → full_metrics.json → audit)
- `scripts/` (최근 30일 626개 파일 변경), `docs/reviews/` (477개)

**목적 한 줄**: DEM 미세구조에서 나온 수송 물성을 **믿을 수 있는 범위와 함께** 보고하는 것.
**활동 기간**: 2026-03-25 최초 커밋 ~ 2026-09-03 · **커밋 2652개**.

### A-2 연구 축
이 브랜치에는 **축이 하나**다 — 축 A (DEM / 저항망). DFT/MLIP 는 없다.

| | 축 A (DEM / MPM / voxelization) |
|---|---|
| 도구·코드 | `dem_scripts/*.liggghts` · `dem_scripts/oat_sweep/` (LIGGGHTS) / `scripts/network_conductivity.py` (Kirchhoff) / `scripts/run_network_full_corrections.py` (Stage E) / `scripts/audit_validation_flags.py` · `pca_ensemble_variance.py` · `plot_porosity_4panel.py` / `webapp/app.py` (Flask 케이스 브라우저 + 3D 뷰어) / `heckel/` · `se_curve/` · `machine-learning/` · `pipeline/` · `이종기술/eis/` / `skills/dem-analysis-{standard,bimodal}.md` |
| 대상 시스템 | NCM811 AM bimodal (D12 / D4) · Li₆PS₅Cl SE (D1) · `am_wt`/`se_wt` 62/38 – 72/28 · P:S 비 0:10 – 5:5 |
| 관심 물리량 | porosity · percolation · σ_ionic · σ_e · σ_th · 배위수 · τ · 접촉력 · 파괴 비율 · ASR |
| 방법론 쟁점 | 1000× 연화 탄성계수 준정적 압축 · Hooke vs Hertz 등가성 · Auerbach+Lawn 파괴 분류 · Stage E grain 보정(Cronau/Trevisanello/Wang) · high-contrast Laplacian → 7층 방어 · Bruggeman EMT 상한 · SE–SE 입계저항 · **regime 밖 편차를 fit 하지 않는다** |
| 진행 상태 | 원고 초안 전 섹션 있음 · 공저자 편집 시트 진행 · LHS 스윕 8개 · litdb 흡수 CL-60~65 |

⚠ **MPM 과 voxelization 은 1급 코드로 확인되지 않았다.** `docs/codex_dem_mpm_response_20260811.md`
같은 리뷰 응답과 litdb digest(`devaucorbeil2020_mpm_after_25_years_review.md`, duquesnoy2020
calendering **voxel** 생성기)로만 나타난다. **문헌·검토 단계로 보이나 unknown.**

### A-3 산출물 인벤토리
| 종류 | 경로 | 한 줄 | 상태 |
|---|---|---|---|
| 시뮬레이션 케이스 | `webapp/archive/<campaign>/<case>/` (atoms.csv + contacts.csv) | DEM 압축 케이스 | **git 추적 안 됨** (README 가 존재를 가정) |
| 케이스별 정본 | `full_metrics.json` (케이스마다 1개) | "single source of truth per case" | **git 에 0개** — repo 밖 |
| 후처리 코드 | `scripts/` | Stage E · audit · PCA · 플롯 | 활발 |
| 집계 표 | `all_dem_porosity.csv` (80케이스) · `validation_all_cases.csv` (80) · `docs/db/section7_10case_sweep.csv` (10) | CSV, 기계 판독 가능 | 활발 |
| 논문 원고 | `docs/paper/main.tex` + `refs.bib` | Stage E 논문 (섹션은 §4 표 참조) | 초안 전 섹션 · 편집 중 |
| 공저자 문서 | `docs/manuscript/Methods_simulation_v7_for_coauthors.docx` · `docs/manuscript_draft/DEM_methodology_and_tables_v1.docx` | Methods 기여 | rev7 |
| 문헌 DB | `litdb/papers/*.md` **64편** · `INDEX.md` · `NOVELTY.md` · `our_dem_baseline.md` · `comparison_vs_ours.md` | Markdown digest | 활발 |
| 리뷰 사슬 | `docs/reviews/` (최근 30일 477파일) · `docs/codex_*.md` | 외부·내부 감사 응답 | 활발 |
| 스킬 | `skills/dem-analysis-standard.md` · `skills/dem-analysis-bimodal.md` | DEM 분석 스킬 | — |
| 그림 | `porosity_4panel.png` · `porosity_main_figure.png` · `validation_all_cases.png` 등 루트 8개 | 원고 그림 | — |

### A-4 살아있는 것 (최근 30일)
1. **원고 본문을 DB 로 내리기** (2026-09-03, 최신 커밋) — 본문 스냅샷 + 판간 diff + 문장별 판정
2. **LHS 스윕** — 미실행 8개 판정 → "게이트를 걸지 않는다, 8개 전부 돌린다 (저자 지시)",
   그 뒤 "장부가 12건을 빠뜨렸고 감시기가 그것을 읽고 있었다" 부수 결함
3. **litdb 흡수 CL-60 ~ CL-65** — Duquesnoy 2020(ML 타깃 하나가 항등식) · Cronk 2026 ·
   Koo SI · adma 판정
4. **편집 시트** §2-4 · §4-3b — 공저자 DOCX 의 죽은 주장, 실측 필드 표가 S17/S18 헤드라인을 바꿈
5. **SDCP 전도도 판별 팔 사전등록** (σ_SDCP = 0) + 스윕 §7-0b/7-0c (런 중 코드 갱신 금지)

TODO·미결: `docs/TODO_post_stage_e_rerun.md` · `docs/backlog_solved_vs_todo.md` ·
`docs/contradiction_audit_20260720.md` (전문은 읽지 않았다 — unknown)

### A-5 확보된 수치 — **미세구조·수송 계열**
**형식: CSV, 기계 판독 가능.** 다만 **케이스별 정본(`full_metrics.json`)은 git 밖**이라
repo 만으로는 재현할 수 없다.

`docs/db/section7_10case_sweep.csv` (10 케이스, 헤더 19열):
| 물리량 | 범위 | 단위 |
|---|---|---|
| porosity_pct | 15.0 – 18.9 | % |
| percolation_pct | 92.3 – 99.6 | % |
| sigma_ionic_mScm | 0.117 – 0.173 | mS/cm |
| sigma_e_mScm | 3.18 – 4.63 | mS/cm |
| sigma_th_mScm | 3.42 – 4.33 | mS/cm |
| AM_percolation_pct | 92.3 – 99.7 | % |
| total_severe_pct (파괴) | 0.0 – 1.23 | % |
| AM_AM_CN_mean | 2.73 – 3.86 | — |
| SE_SE_CN_mean | 4.39 – 5.24 | — |
| tau_Lap_eff | 1.21 – 4.39 | — |
| F_DEM_AM_P_AM_P_mN | 1.32 – 9.04 | mN |
| F_over_Pc_AM_P_AM_P | 1.319 – 9.036 | — |

`all_dem_porosity.csv` · `validation_all_cases.csv` — **80 케이스**:
설계 변수 `am_wt` `se_wt` `p_vol` `s_vol` `n_AM_P` `r_AM_P_um` `n_AM_S` `r_AM_S_um` `n_SE` `r_SE_um` `scale`,
결과 `porosity_pct` 16.365 – 19.732 %, 예측 `eps_pred`, `residual` −2.91 – +1.52 %p

⚠ README 는 "167-case analysis" 와 "82-case ensemble" 을 말하는데 **git 의 CSV 는 80행**이다.
판이 갈렸거나 일부가 repo 밖이다 — **unknown.**

**원자 스케일 계열**: 이 브랜치에 **없다.**

---

## 3. 두 브랜치 종합 (A-6)

| | 브랜치 A `friendly-meitner-lldvar` | 브랜치 B `stoic-knuth-NObVQ` |
|---|---|---|
| 축 | B (DFT / MLIP) | A (DEM / 저항망) |
| 커밋 | (조사 안 함) · 최신 2026-09-03 | **2652** · 2026-03-25 ~ 2026-09-03 |
| 원고 | AF-ASSB AgNO₃–C–PVP SI 기여 (.docx) | Stage E 저항망 논문 (main.tex, 1저자) |
| 수치 형식 | JSON + canonical_registry (39항목) | CSV (80 + 10 케이스) |
| litdb | 208편 | 64편 |
| 웹앱 | 정본값 뷰어 | 케이스 브라우저 + 3D 뷰어 |

- **분기점**: **없다.** `git merge-base` rc=1. 두 개의 독립 루트 커밋.
- **역할 분담**: 완전 분리. 공유 코드 0.
- **겹침**: ① 둘 다 `litdb/` 를 갖는다 (별개 인덱스 — 브랜치 B 커밋이 *"내 중복 확인 방법이 틀렸다
  — litdb 인덱스가 셋이다"* 라고 적고 있다). ② 둘 다 Li₆PS₅Cl 을 다루지만 **스케일이 다르다**
  (원자 vs 입자). ③ 둘 다 공저자용 Methods .docx 를 낸다 (v7 / v8).
- **통합 필요 여부**: **아니다.** merge 하면 2652 커밋과 무관 히스토리가 섞이고 얻는 것이 없다.
  다만 **litdb 만은 겹친다** — 고유 DOI 195개 중 A 199 / B 61 이라 상당수가 중복이다.
  research-agent 가 두 곳에 다 써야 하는지, 한 곳을 정본으로 삼을지 **결정이 필요하다.**
- **전체 그림**: 한 사람이 **같은 재료계(황화물 ASSB)를 두 스케일에서 따로** 공격한다. 원자
  스케일에서는 "이 값을 인용해도 되는가" 를 절차로 닫고, 입자 스케일에서는 "이 파이프라인이
  언제 틀리는가" 를 방어층으로 닫는다. **공통점은 물리가 아니라 방법론적 엄격성**이다 — 양쪽
  모두 사전등록·게이트·자기보고·외부 감사 사슬을 갖고 있다. 두 축을 잇는 것은 파이프라인이
  아니라 **연구자의 작업 방식**이다.

---

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

안용훈은 **한 재료계(황화물 ASSB)를 두 스케일에서 따로 공격하는 사람**이다. 브랜치
`stoic-knuth-NObVQ` 에서는 LIGGGHTS DEM 패킹 → Kirchhoff 저항망 → Stage E 파괴/grain 보정으로
porosity·σ·ASR 를 내고(2652 커밋, 원고 초안 전 섹션 완비), 브랜치 `friendly-meitner-lldvar`
에서는 VASP·QE·UMA·ORCA 로 밴드갭·탄성·ICOHP·NEB 장벽·바인더 흡착을 낸다(정본 39항목). 두
브랜치는 **git 공통 조상이 없고** 코드를 공유하지 않으며, 접점은 공저자용 Methods 문서 한 쌍뿐이다
— Cowork 가 쓴 "하나의 multi-scale 파이프라인" 은 틀렸다. 두 축을 잇는 것은 물리가 아니라
**작업 방식**이다: 양쪽 다 계산 전에 보고량을 정의하고, 게이트를 결과 보기 전에 박고, 못 확인한
것을 통과로 세지 않으며, 외부 감사 사슬을 돌린다. 따라서 research-agent 가 이 사람에게 쓸모
있으려면 **논문을 많이 물어오는 것이 아니라, 이미 읽은 것을 다시 올리지 않고(8-2), 사용자의 실제
litdb 에 쓰고(8-1), 진행 중인 두 주장이 선점당할 때 경보를 울려야(#2)** 한다. 지금 가장 큰
구조적 기회는 §5 가 보여준 비대칭이다 — **내 수치는 이미 기계 판독 가능한데 문헌 수치만
Markdown 표에 갇혀 있다.** 그 표는 이미 4열로 표준화돼 있으므로, 수치DB(#1)는 새 데이터 수집이
아니라 **파싱 문제**다.

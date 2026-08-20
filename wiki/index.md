# Wiki Index — Yonghoon-DEM-DFT

> 지식 지도.  모든 페이지가 타입별로 한 줄 요약과 함께 등록된다.
> 규칙: `wiki/SCHEMA.md` · 점검: `python3 wiki/tools/lint.py`
> Last updated: 2026-08-11 | Total pages: 21

## Concepts (핵심 개념 — 여러 세션에 걸쳐 반복 참조)

- [[frame4-independent-calibration]] — DEM↔MPM 상호 보정 금지: 각자 실험에만 보정, 수렴=교차검증·발산=정량화된 한계.
- [[frame5-division-of-labor]] — 분업 지도: DEM=접촉망σ·패킹·dip / MPM=형상·void-fill / 둘 다=porosity·coverage.
- [[ese-softening-18x]] — E_SE 24→1.35/1.53 유효연화: 3중 확인 + 되돌리기 3중 실패 = 환원 불가 (단 bulk 축은 ν=0.49 로 복원).
- [[quasistatic-platen-gate]] — V/c_P≤0.01 게이트: 위반 런은 등급 B(상대비교 전용), metrics JSON 이 위반을 달고 다닌다.
- [[dh-collapse]] — 다섯 침대 σ(φ) 를 d_h=V_free/S_AM 하나로 접기: R² 만 해상도 불변, 기울기는 하한.
- [[sr01-stamp-fragmentation]] — STEP3 점-스탬프가 섬유를 20.6–75.8 % 조각냄: 해결=선분 스탬프, Δσ_e 는 측정으로만.

## Entities (시스템·자원)

- [[dem-webapp-pipeline]] — LIGGGHTS + 접촉망 Kirchhoff/Holm σ + 대시보드 (σ 폼 3종 동결).
- [[mpm-kit-pipeline]] — 킷 zip → scaffold 압밀 → payload → STEP3/4 (킷과 웹앱은 코드가 따로).
- [[se-curve-kits]] — P:S 조성만 다른 대조군 침대 5종 + 보존/복원 도구.
- [[litdb-canon]] — 논문 카드 단일 서랍 (friendly-meitner 브랜치; 이 브랜치 litdb/ 는 동결).
- [[findings-ledger]] — 리뷰 발견 원장 findings.json (SR/RC, claimed_fixed ≠ verified).
- [[llm-wiki-kit-origin]] — 이 위키의 출처 킷(v1.7)과 개조 내역 (model-ID 금지·litdb 경계·5축).

## Comparisons

- [[network-vs-voxel-sigma]] — σ 솔버 2종: 접촉망(DEM) vs 복셀 FV(STEP3) = 독립 이중 측정, 파이프라인 분리 주의.

## Guides (절차)

- [[kit-run-protocol]] — V100 부트스트랩→worktree→게이트 배선→run_mpm→완료판정→A/B (드립 재발 방지).
- [[adversarial-review-protocol]] — 3각 자체리뷰 + Codex 교차 + 원장 등재 + 수치는 하네스와 커밋.
- [[litdb-canon-procedure]] — 정본 카드 조회/추가 워크트리 절차 (INDEX 먼저, 복사 금지).
- [[context-compaction-policy]] — 50 %에 알리고 압축은 사람이. `autoCompactWindow` 금지 + 계기 3가드.

## Questions (열린 질문 — 자료가 올 때마다 근거 축적)

- [[sr01-delta-sigma-sign]] — (active) 점→선분 래스터 교체 시 Δσ_e 부호·크기: A/B 하네스 완성, 측정 대기.
- [[dh-288-protocol-equalization]] — (active) 8런 대등화가 φ-선택 감도를 없애는가 (§⑩ 규칙 검증).
- [[anchor-waitlist]] — (open) §F1 앵커 대기 큐: Joule ΔT·코팅 √N·SDCP E_bind·NCA E175·EIS C_dl/R_w.

## Syntheses (논지 방어)

- [[dem-transport-mpm-mechanics]] — "DEM=수송/패킹, MPM=형상/소성" — 2026-08-11 정정을 거쳐 더 정밀해진 논지.

## Queries

(아직 없음 — /wiki-query 의 file-back 으로 채워진다)

---

## 미이관 코퍼스 분류 (docs/ → 위키 타입 매핑, 이관 백로그)

> 정본 서술은 아래 문서들이다.  위키 페이지가 없는 동안에도 이 표가 내비게이션
> 역할을 한다.  이관 기준: 여러 세션에서 반복 참조되기 시작하면 페이지로 승격.

| 문서 | 타입 후보 | 요지 |
|---|---|---|
| docs/se_curve_transfer_verdict_20260806.md | synthesis+RQ | SE 곡선 베드-전이 기각 → d_h 접힘 (§①~⑩) — 일부는 [[dh-collapse]] 로 승격됨 |
| docs/mpm_platen_kinematic_stop_defect.md | concept | 플래튼 비준정적 하강·운동학적 정지 결함 — [[quasistatic-platen-gate]] 의 정본 |
| docs/mpm3d_calibration.md | entity/concept | 3D MPM 3-fix 보정 + scaffold 교차검증 |
| docs/mpm_dem_wallP_crossvalidation.md | comparison | 132 케이스 wallP 대조: CORRECTION 1(soft-bulk)·2(dip 미재현) |
| docs/mpm_dpc_cap_crosscheck.md | comparison | DPC cap 기각 — 연화 환원 불가의 소성 축 증거 |
| docs/esse_calibration_2mAh_real_9.md | concept | E_SE 1.35 KEEP 판정 + ε_sphere 규약 |
| docs/mpm_scaffold_reliability_and_am_freeze.md | concept | porosity 신뢰 regime map + AM 동결 4근거 |
| docs/mpm_coverage_plastic_vs_rigid.md | concept | coverage 2측정(rigid/plastic) 규약 — voxel-adjacency 보고 금지 |
| docs/sulfide_se_mechanical_anchors.md | concept | Fan §3.5 대조: K_IC→G_c 이중화·입경 닫힌 설계창 |
| docs/sigma_ionic_physics_derivation.md | concept | σ_ionic 폼 유도·동결 근거 (재적합 금지) |
| docs/ionic_scaling_law_experiments.md | concept | v12-clean v3 계보 (3 이름 1 모델) |
| docs/manuscript_sdcp_sigma_e_mechanism.md | synthesis | SDCP σ_e 기전 원고 — ⛔ **HISTORICAL** (옛 +52 % 헤드라인은 2026-08-13 철회, CL-24) |
| docs/project_rint_fullcell_cycling.md | entity | R_int 풀셀/사이클 프로젝트 정본 |
| docs/step4_v2_design.md | entity | STEP4-v2 갈바노/CV 설계 (PyBaMM 패리티 대기) |
| docs/a10_cycle_chemomech_design.md | entity | A10 사이클 화학-기계 원장 (poly-mode 정정 포함) |
| docs/real_degrading_electrode_design.md | entity | 열화 전극 설계 (N6-b: shrink-proxy 아티팩트) |
| docs/temp_pressure_capability.md | concept | 온도·압력 축 스코프 (제작압 vs 구동압 혼동 가드) |
| docs/nca_material_preset.md | concept | NCA 프리셋 — E175 검증 차단 경위 |
| docs/ncm_sc_poly_electrochem_anchors.md | concept | SC/PC 앵커 41건 (ASSB 역전) |
| docs/defense_review_20260720.md | synthesis | COMSOL-대체 verdict |
| docs/plan_vgcf_ptfe_coupling_20260811.md | query | VGCF/PTFE 계획서 (P1/P2 승인·P3 보류) |
| docs/plan_se_grad_20260811.md | query | --se-grad 계획서 (G4→G1 순) |
| docs/lab_ai_workflow_conventions.md | guide | 랩 AI 워크플로 규약 (figure format·reference 규칙) |
| docs/lit_*.md (Varkey·Bazzoun 등) | (litdb) | litdb 이전 시절 digest — 신규는 정본 서랍으로 |

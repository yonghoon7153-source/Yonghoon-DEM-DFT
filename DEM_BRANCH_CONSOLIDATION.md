# DEM 브랜치 통합 (2026-06-07)

흩어져 있던 **DEM 계열** 작업을 한 브랜치(`claude/stoic-knuth-NObVQ`)로 통합한 기록.
**ML/DFT 계열과 standalone 프로젝트는 의도적으로 분리 유지** (형님 지시).

## 결론 요약

- **Base = `claude/debug-fracture-solver-DQE6G`** (356 files, 2026-06-07) — DEM 계열 중
  가장 최신·가장 완전한 상위집합(superset). CLAUDE.md 상단 DEM-MPM 상보 frame,
  167-case porosity validation, 전체 파이프라인, webapp, 논문 draft 포함.
- DEM 형제 브랜치 11개를 모두 합쳐도 DQE6G에 **없던 고유 파일은 단 40개**,
  그중 의미 있는 것은 LqBv3의 **전자전도도 스케일링 스크립트 39개**뿐이었음.
  → 이 39개를 DQE6G 위에 얹어 통합 완료. (나머지 1개는 `__pycache__/*.pyc` — 제외)

즉 **DQE6G ≈ 이미 DEM 통합본**이었고, 이 브랜치는 거기에 빠진 전자전도도
실험 묶음만 보강한 것.

## 통합 내용

### Base (그대로 승계)
`claude/debug-fracture-solver-DQE6G` 전체 — fast-forward 머지.
- `scripts/` 약 230개: `fracture_model.py`, `network_conductivity.py`,
  `run_network_full_corrections.py`, `run_network_fracture_aware/stagewise.py`,
  `physics_fit_v33~v60`, `thermal_*`, `electronic_*`(DQE6G 자체 계열),
  `mpm2d_*/mpm3d_compaction.py`, `heckel_analysis.py`,
  `compare_laplace_dijkstra.py`, `triage_cases.py`, `viewer3d_data.py` 등
- `webapp/` (Flask): `app.py`, `viewer3d.js`, templates 7종, `predictor_engine.py`,
  `pybamm_predictor.py`, `storage_sync.py`
- `dem_scripts/` LIGGGHTS 입력, `heckel/` 압력 sweep 입력
- `docs/`: 논문 draft(`docs/paper/`), 각종 derivation, Reviewer Defence Notes,
  Tabor framework 등
- **db / 데이터**:
  - `docs/db/section7_10case_sweep.csv`
  - `docs/data/` (esse calibration, percolation 2D fit)
  - `docs/literature_coverage/` — `contact_mechanics_db.json`, `coverage_db.json`,
    `packing_regime_db.json` + 논문 PDF 4편 (Bouvard 2000, Martin-Bouvard 2003,
    McGeary 1961, So 2021)
  - 루트 `all_dem_porosity.csv`, `validation_all_cases.csv`, `docs/full_ranking.csv`,
    `docs/case_summary.csv`

### 추가로 folded-in (LqBv3 출처)
전자전도도(σ_e) 스케일링-법칙 스크리닝 실험 묶음 **39개**:
- `scripts/electronic_scaling_law.py`
- `scripts/screening_electronic*.py` (37개 변형: clean / deep / final / perfect /
  radical / thin_* / unified / universal 등)
- `scripts/stress_test_el_th.py`

> 참고: 이 묶음은 DQE6G 자체의 `electronic_*` 계열과는 **별개의 실험 흐름**
> (LqBv3 "SE Diagnostics" 세션 산출물). 보존 차원에서 전부 가져옴 — 추후 정리/삭제는
> 형님 판단.

## 검토 필요 — 같은 경로, 다른 내용 (자동 머지 안 함)

아래는 일부 형제 브랜치가 **DQE6G와 동일 경로에 다른 버전**으로 가진 webapp 로직.
DQE6G가 최신(2026-06-07)이라 **DQE6G 버전을 채택**했고, 아래 변형은 머지하지 않음.
필요하면 개별 기능만 골라 이식 가능:

| 브랜치 | 동일 경로 변형 | 성격 |
|--------|----------------|------|
| `stagewise-fracture-solver-3VvPg` | `webapp/.../viewer3d.js`, `single.html` | FORCE-based brittle classifier UI (DQE6G 파이프라인이 이미 force 기반이라 사실상 흡수됨) |
| `resistor-network-paper-bc5yi` | `webapp/app.py` | defense-mode UI / atoms-only 파싱 (관련 스크립트 `triage_cases.py`, `compare_laplace_dijkstra.py`는 DQE6G에 이미 존재) |
| `debug-fracture-solver-LqBv3` | `webapp/templates/*` | corpus-percentile SE 진단 stats card |

## 전체 브랜치 분류

### A. DEM 계열 → **본 브랜치로 통합 완료**
DQE6G(base) + LqBv3(screening) 흡수. 나머지는 DQE6G의 부분집합/구버전:
`stagewise-fracture-solver-3VvPg`, `resistor-network-solver-LDjW6`,
`resistor-network-paper-bc5yi`, `resistor-network-analysis-UGoNB`,
`resistor-network-analysis-lKgcS`, `add-metric-cards-0a3n0`,
`reconnect-dem-website-ubGVZ`(고유 0), `organize-network-metrics-KEivv`,
`optimize-dem-analysis-Nap1m`, `add-bulk-operations-KddvJ`.

### B. ML/DFT 계열 → **분리 유지 (건드리지 않음)**
Argyrodite mechanical / adhesion / doping / NEB 연구 (Vite 앱 + `db/` + `kb/` +
`runs/` + `필독/`):
- `claude/unified-2026-05-15` (393, 2026-06-01) — 기존 통합 base
- `claude/configure-spawn-halogen-lithium-TjDCB` (227, 2026-06-06) — **현재 active**,
  unified에 없는 고유 콘텐츠 보유: `modelc_v3.json`, interphases(`li3n/lic6`),
  `diffusion.json`, `li_transport.json`, tools 46개(`neb_diffusion/`, `modelc_v3/`,
  `doping/` B₂O₃)
- `review-ml-migration-W29af` (231), `review-ml-migration-1BN1c` (130),
  `argyrodite-ml-migration-kDtHW` (89), `argyrodite-ml-prediction-ozuoX` (57)
- ⚠️ 이름 오해 주의: `debug-api-500-error-iukkt`(358), `debug-api-500-error-u8KI7`(232)는
  "api 디버그"가 아니라 **Argyrodite ML/DFT** 브랜치 → ML/DFT 계열로 분류.
- ⚠️ unified ↔ configure-spawn 가 5/15 이후 **분기 상태** → ML/DFT 쪽도 별도 통합 필요
  (이번 작업 범위 밖).

### C. Standalone 프로젝트 → **별개 (DEM 연장선 아님)**
- `dft-script-generator-webapp-GPSAG` (39) — React DFT 스크립트 생성기
- `notion-database-chatbot-PJA1x` (33) — React+Express Notion 챗봇
- `market-research-presentation-bC9Yi` (44) — React 발표자료 앱
- `ssb-market-research-ZiEJ4` (1) — `refs/SSB_reference_DB.md`
- `lammps-bimodal-cathode-fhdp6` (3) — LAMMPS VGCF 단섬유 테스트
- `linear-regression-lecture-DaaRi` (5) — ML 강의노트
- `review-skills-create-branch-HPzBW` (3) — `liggghts-dem-analysis` 스킬

## 비고

- **실제 DEM 케이스 데이터**(`webapp/archive/<campaign>/*/atoms.csv,contacts.csv,
  full_metrics.json`)는 git에 커밋돼 있지 않음 (`.gitignore`, 용량). 서버/로컬에만 존재.
  파이프라인 재현 시 README의 archive 가정 참고.
- 모든 원본 브랜치는 그대로 보존됨 (이 통합은 비파괴적). 추후 archive 태그/삭제는
  형님 결정.

---
**통합 브랜치**: `claude/stoic-knuth-NObVQ` (base = `claude/debug-fracture-solver-DQE6G`)
**작성**: 2026-06-07

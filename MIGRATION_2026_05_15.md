# MIGRATION 2026-05-15 — branch unification

세션 컨텍스트 한계로 분기됐던 두 작업 흐름을 통합한 기록.

## Background

- `claude/review-ml-migration-W29af` (canonical, 231 files, 필독/ + db/ + kb/
  + runs/ + tools/ + webapp) — 별도 클로드 세션의 큰 그림.
- `claude/configure-spawn-halogen-lithium-TjDCB` (30 files) — 본 세션의 작업
  (literature DB, doping pipeline, mechanical pipeline doc, LPSCl baseline CIF).
- `main` — Initial commit only.

두 브랜치가 자동 머지 시 README 등에서 충돌 → 충돌 회피 위해 W29af 위에 우리
파일만 수동으로 cherry-place. 결과: `claude/unified-2026-05-15`.

## File mapping (configure-spawn → unified)

### 1. Literature DB
| 원본 위치 | 새 위치 |
|-----------|---------|
| `kb/literature_db/damore_2022_lpscl_symmetry_breaking_qha.md` | `db/literature/damore_2022_lpscl_symmetry_breaking_qha.md` |
| `kb/literature_db/pustorino_2025_lpscl_li_ordering_mechanical.md` | `db/literature/pustorino_2025_lpscl_li_ordering_mechanical.md` |
| `kb/literature_db/sundar_2025_lpscl_coating.md` | `db/literature/sundar_2025_lpscl_coating.md` |

→ W29af의 `db/literature/` convention 채택 (기존에 `refs.json`, `zhao2025_critique.md` 존재).

### 2. Knowledge base — methodology/papers
| 원본 | 새 위치 |
|------|---------|
| `kb/methodology/argyrodite_mechanical_pipeline.md` | 동일 ⭐ canonical 8-step + appendix |
| `kb/methodology/doping_substitution_algorithm.md` | 동일 |
| `kb/descriptors/coating_descriptor_catalog.md` | `kb/methodology/coating_descriptor_catalog.md` |
| `kb/platforms/literature_db_tools.md` | `kb/methodology/platforms_literature_db_tools.md` |
| `kb/platforms/ml_automation_platforms.md` | `kb/methodology/platforms_ml_automation.md` |
| `kb/projects/digital_twin_roadmap.md` | `kb/methodology/digital_twin_roadmap.md` |
| `kb/papers/mechanism_anion_O_descriptor.md` | 동일 (v0 paper mechanism) |
| `scripts/PHASE1_QUICKSTART.md` | `kb/methodology/PHASE1_QUICKSTART_doping.md` |

→ `kb/descriptors/`, `kb/platforms/`, `kb/projects/` 폴더는 W29af에 없음 → 모두
`kb/methodology/`로 통합.

### 3. Doping pipeline scripts
| 원본 | 새 위치 |
|------|---------|
| `scripts/doping/site_preference.py` | `tools/doping/site_preference.py` |
| `scripts/doping/substitute_struct.py` | `tools/doping/substitute_struct.py` |
| `scripts/doping/run_uma_screening.py` | `tools/doping/run_uma_screening.py` |
| `scripts/doping/analyze_screening.py` | `tools/doping/analyze_screening.py` |
| `scripts/doping/fetch_mp_structure.py` | `tools/doping/fetch_mp_structure.py` |
| `scripts/doping/dopant_candidates.json` | `db/doping/dopant_candidates.json` |
| `data/doping_screening/site_preference_initial.json` | `db/doping/site_preference_initial.json` |
| `data/lpscl_bulk.cif` | `db/structures/lpscl_bulk.cif` |

→ `tools/` = utility scripts, `db/` = data/structures/configs.

### 4. v0 paper adhesion analysis
| 원본 | 새 위치 |
|------|---------|
| `scripts/adhesion/alpha_sensitivity_FINAL.py` | `필독/adhesion/alpha_sensitivity_FINAL.py` |
| `scripts/adhesion/bond_density_36reg_FAST.py` | `필독/adhesion/bond_density_36reg_FAST.py` |
| `scripts/adhesion/bond_density_LiO_cutoff_sweep.py` | `필독/adhesion/bond_density_LiO_cutoff_sweep.py` |
| `scripts/adhesion/comprehensive_FINAL_analysis.py` | `필독/adhesion/comprehensive_FINAL_analysis.py` |
| `scripts/adhesion/generate_stacked_deq_orthogonal.py` | `필독/adhesion/generate_stacked_deq_orthogonal.py` |
| `scripts/adhesion/plot_R0988_TIGHT_FIT.py` | `필독/adhesion/plot_R0988_TIGHT_FIT.py` |
| `scripts/adhesion/run_li_migration_FINAL_combo.py` | `필독/adhesion/run_li_migration_FINAL_combo.py` |

→ `필독/adhesion/` 에는 이미 `phase2a_v10~v31_*.py` 시리즈 (W29af 유래)가 있고,
우리 FINAL 분석 스크립트들이 보완 관계.

### 5. UMA EOS pre-DFT (Nd doped paper #2)
| 원본 | 새 위치 |
|------|---------|
| `scripts/adhesion/uma_screen_all_pairs.py` | `runs/nd_doped_modelc/2_uma_eos_predft/uma_screen_all_pairs.py` |
| `scripts/adhesion/uma_eos_pre_dft.py` | `runs/nd_doped_modelc/2_uma_eos_predft/uma_eos_pre_dft.py` |
| `scripts/adhesion/sbatch_uma_eos_kisti.sh` | `runs/nd_doped_modelc/2_uma_eos_predft/sbatch_uma_eos_kisti.sh` |

### 6. DFT EOS (Nd doped paper #2)
| 원본 | 새 위치 |
|------|---------|
| `scripts/adhesion/prepare_dft_eos_nd.py` | `runs/nd_doped_modelc/3_dft_eos/prepare_dft_eos_nd.py` |
| `scripts/adhesion/sbatch_dft_eos_nd.sh` | `runs/nd_doped_modelc/3_dft_eos/sbatch_dft_eos_nd.sh` |
| `scripts/adhesion/run_dft_eos_pair.sh` | `runs/nd_doped_modelc/3_dft_eos/run_dft_eos_pair.sh` |

### 7. Tools — automation
| 원본 | 새 위치 |
|------|---------|
| `scripts/automation/literature_harvest.py` | `tools/literature_harvest.py` |

## Not migrated (intentional)

- `README.md`, `TIMELOG.md` — W29af의 (React template) README와 충돌, 별도 정리 필요.
  W29af README는 사실 React+Vite 템플릿 그대로 → 진짜 프로젝트 README는 다음 세션에서
  통합 작성 권장.
- `scripts/automation/` 빈 디렉토리 — 안 옮김.
- `scripts/descriptors/` 빈 디렉토리 (W29af에도 동일 위치 빈 폴더 존재).

## Branches — 처리 권장

| 브랜치 | 권장 처리 |
|--------|-----------|
| `claude/unified-2026-05-15` ⭐ | **다음 작업의 base** |
| `claude/configure-spawn-halogen-lithium-TjDCB` | archive tag 후 삭제 가능 (모든 작업이 unified에 옮겨짐) |
| `claude/review-ml-migration-W29af` | 보존 (canonical 원본, archive 태그 권장) |
| `claude/review-ml-migration-1BN1c` | 거의 동일, archive 태그 |
| `claude/argyrodite-ml-migration-kDtHW`, `claude/argyrodite-ml-prediction-ozuoX` | 더 오래된 버전, archive 태그 |
| `claude/dft-script-generator-webapp-GPSAG` | webapp 전용 — 별도 repo 분리 권장 |
| 그 외 `claude/*` 브랜치 ~15개 | 작업 끝났으면 archive 태그 또는 삭제 |

archive 명령 예시 (실행 전 형님 승인 필요):
```bash
for br in claude/review-ml-migration-W29af claude/review-ml-migration-1BN1c \
          claude/argyrodite-ml-migration-kDtHW claude/argyrodite-ml-prediction-ozuoX; do
    git tag -a "archive/${br//\//-}" "origin/$br" -m "archived 2026-05-15"
done
git push origin --tags
```

## 검증 체크리스트

- [x] 모든 파일이 새 위치에 존재 (22개 신규 path)
- [x] CODE_INVENTORY.md 에 Z 섹션 추가
- [ ] gabia에서 `git pull` 후 `tools/doping/site_preference.py --validate` 통과 확인 (사용자 작업)
- [ ] 옛 브랜치 archive 태그 (사용자 결정 후 실행)

## 다음 세션 첫 작업 권장

1. `cat CLAUDE.md CODE_INVENTORY.md MIGRATION_2026_05_15.md` 읽기 (W29af의 CLAUDE.md 규칙 그대로)
2. 가비아 UMA 풀 런 결과 (`data/doping_screening/uma_screening_results.json`)를 `runs/doping_screening_2026_05_15/`로 복사
3. `analyze_screening.py`로 Top-N 분석
4. 형님이 보여준 layout에서 빠진 슬롯 (`db/properties/`, `kb/results/section3` 등) 채우기

---

**작성**: 2026-05-15
**브랜치**: `claude/unified-2026-05-15` (base = `claude/review-ml-migration-W29af`)

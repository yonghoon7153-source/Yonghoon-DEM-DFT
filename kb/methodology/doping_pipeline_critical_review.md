# Doping Pipeline — Critical Self-Review (2026-05-16, v4 championship)

본 문서는 **새 세션에서 첫 5분 안에 읽어** 우리 도구가 무엇을 잡고
무엇을 놓치는지 즉시 파악할 수 있게 작성. CODE_INVENTORY.md와 같이 읽기.

---

## 1. 도구 현황 (16 files in `tools/doping/`)

### Substitution
| 도구 | 역할 |
|------|------|
| `site_preference.py` | 75+ DOPANT_DB, 19 multi-valence, CN-aware radii, --validate 0/19 |
| `substitute_struct.py` | spread/random/cluster/first/near_cation, PBC farthest-point |
| `substitute_compound.py` | Type A/B/B'/C/D, auto-valence, Li interstitial for acceptor |
| `run_compound_batch.sh` v3 | ~85 compounds × 9 sites × 5 seeds 자동 batch |

### Screening
| 도구 | 역할 |
|------|------|
| `run_uma_screening.py` | UMA relax + Tier-1 (ΔE/atom, ΔV) + Tier-2 (5 cheap metrics) + outlier guard + provenance |
| `select_winners.py` | per-(compound, sites) Top-1 추출 |
| `bvse_proxy.py` | per-Li BVS + Li migration volume fraction |

### Post-processing
| 도구 | 역할 |
|------|------|
| `run_anneal.py` | Langevin MD + relax, 4 input modes, --light/--per_compound_top |
| `rank_anneal.py` | pre/post anneal ranking flip detection |
| `run_mlip_postproc.py` | EOS BM3 fit + finite-strain Cij + VRH (B/G/E/Pugh/ν) |
| `analyze_screening.py` | 5 objective (composite/binding_E/formation_E/per_dopant/disorder) |
| `combine_rankings.py` | 7-stage chain → unified multi-axis ranking |
| `generate_dft_inputs.py` | Top-N → QE pw.in (Tier-4 paper-grade) |

### Infrastructure
| 도구 | 역할 |
|------|------|
| `_provenance.py` | env metadata (python/ase/uma/git versions) |
| `preflight.py` | 4 sanity checks 전 batch 시작 |
| `tier_cascade.sh` v2 | 10-stage factory line + STAGE_NN.DONE 마커 |
| `watch_status.sh` | 실시간 dashboard |

---

## 2. 지금 잘 다루는 것 (검증됨)

- 85+ compound 종류 (mono~hexa oxide, fluoride, chloride, bromide, iodide,
  nitride, sulfide, polyanion)
- 19 multi-valence 원소 (CrO3/MnO2/Fe3O4/Bi2O5 등 자동 처리)
- 5 doping type (single/halide-rich/mixed-halide/chain/high-entropy)
- True farthest-point spread (PBC-aware), cluster (PS4→PO4), near_cation
- Li vacancy (donor) + Li interstitial (acceptor) 둘 다 charge balance
- Multi-supercell (1x1x1, 2x1x1, 2x2x1, 2x2x2)
- 5 ranking objective + 5 Tier-2 metric + BVSE proxy
- 7-stage cascade with resume markers
- Provenance + outlier guard + reproducibility

---

## 3. 솔직히 놓치는 것 (TODO 우선순위)

### ⚠ 즉시 critical (paper-grade 위해 필수)

1. **MLIP bias 검증 안 됨** (Wang 2025 npj Comp Mater: UMA류 general MLIP은
   sulfide PES softening + Li diffusivity overestimation 문제 존재)
   → spot-check: comp1/comp5 known DFT B0와 UMA 값 비교 필요
   → 또는 reEWC fine-tuning (Wang 2025 reference)

2. **Mixed-cation 화합물에서 per-cation site routing 미완**
   - 현재 모든 양이온이 같은 site에 (Mg + Al in MgAl₂O₄ → 둘 다 Li_24g)
   - 실제 spinel chemistry: Mg at tetrahedral (Li-like), Al at octahedral
   - Workaround: --auto_cation_sites가 site 다양화는 시도

3. **Formation energy μ JSON 없음**
   - `--objective formation_E` 옵션은 있지만 precursor chemical potential
     dict 없음. MP API로 받아오는 helper 작성 필요.

### Medium impact

4. **Generic vacancy defect** (Li removal 단독, cation 없이)
5. **Antisite defects** (P-S, S-Cl) — D'Amore 2022 reference
6. **Partial occupancy / VCA** — Mg+Li 50:50 같은 자리
7. **SOAP/RMSD structural dedup** (symmetry-equivalent 제거)

### Lower

8. **CN-aware radii 부분 구현** (Li/Na/K/Mg/Zn/Al/Ga/In만 cn4 값 있음)
9. **Polyanion as discrete unit** (PO₄ 그룹이 PS₄ 자리 통째 대체)
10. **Convex hull / Ehull** (MP 통합)

---

## 4. 알려진 외부 의존성 / 가정

- UMA-s-1p1 (FAIRChem) — sulfide-specific fine-tuning 없음, general model
- PBE 수준 정확도 (DFT 수준 아님, B0 계산값에 ~10-20% 절대 오차 가능)
- Shannon ionic radii (1976 + Adams 2003 sulfide refit)
- BVSE parameters (Brown 1985 / Adams 2003 — Li-S, Li-Cl, Li-O 등)
- Argyrodite F-43m baseline (idealized Wyckoff; D'Amore 2022 phonon
  unstable이지만 anneal로 자연 fix)

---

## 5. 1주일 batch 시 failure mode 대비책

| Failure | 대비 |
|---------|------|
| OOM | 메모리 측정 안 함 — 큰 supercell 시 주의 |
| Disk full | preflight 단계 ≥5GB check ✅ |
| Cluster reboot | resume by name 모든 도구 ✅ |
| Process kill | tier_cascade STAGE_NN.DONE 마커로 stage-level resume ✅ |
| Bad baseline | preflight PS4 integrity check ✅ |
| UMA divergence | outlier_flag (|ΔV|>30% 또는 |ΔE|>5 eV/atom) ✅ |
| 잘못된 chemistry | site_preference --validate 0/19 통과 보장 ✅ |
| Insight 없음 | positive control (Nd2O3/La2O3/Al2O3) → 모두 Top tier에 들어야 함 |

---

## 6. 사용 시퀀스 (1 batch 권장)

```bash
# 0. 갱신
cd <repo>
BRANCH=claude/unified-2026-05-15
RAW="https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/${BRANCH}"
for f in $(curl -s "https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/contents/tools/doping?ref=${BRANCH}" | python3 -c "import json,sys; [print(d['name']) for d in json.load(sys.stdin)]"); do
    wget -q -O tools/doping/$f "${RAW}/tools/doping/${f}?nocache=$(date +%s)"
done
chmod +x tools/doping/*.sh

# 1. cascade
nohup bash -c '
source /data/apps/miniforge3/etc/profile.d/conda.sh
conda activate uma
bash tools/doping/tier_cascade.sh \
    db/structures/lpscl_F43m_24G_canonical.cif \
    runs/tier_$(date +%F) \
    5 1,1,1 1
' > logs/cascade.log 2>&1 &

# 2. monitor
watch -n 30 'bash tools/doping/watch_status.sh'

# 3. (cascade 끝나면) DFT inputs for top-10
python3 tools/doping/combine_rankings.py \
    --cascade_dir runs/tier_$(date +%F) \
    --out runs/tier_$(date +%F)/FINAL_RANKING.json
python3 tools/doping/generate_dft_inputs.py \
    --ranking runs/tier_$(date +%F)/FINAL_RANKING.json \
    --top 10 --out runs/tier_$(date +%F)/dft_inputs/
```

---

## 7. 다음 라운드 (이 batch 결과 받은 후)

1. Top-10 → KISTI DFT 검증 (`generate_dft_inputs.py` 출력 그대로)
2. MLIP vs DFT 정량 비교 → UMA bias 보정 또는 reEWC fine-tuning
3. Top-3 → MLIP-AIMD 600K 50ps → 실제 σ_Li 계산
4. Top-3 → 600K snapshot elastic (Cij thermal disorder 포함)
5. Mixed-cation per-site routing 구현 (Wave 5)
6. paper draft

---

**최종 commit hash 확인**: `git log --oneline -3`
**브랜치**: `claude/unified-2026-05-15`
**작성일**: 2026-05-16

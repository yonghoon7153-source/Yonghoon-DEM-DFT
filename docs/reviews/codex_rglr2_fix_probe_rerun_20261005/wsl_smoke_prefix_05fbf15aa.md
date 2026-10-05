# WSL small integration test — PRE-FIX (code 05fbf15aa) · 2026-10-05 21:16–21:18 KST · user DESKTOP-IK8J81H ~/dem-audit
ROOT /home/yonghoon71/net_smoke_05fbf15aa_1005_2116 (smoke_report.json · smoke_summary.txt on WSL)
selftest 10/10 ✓
case            status  wall_s pipeline_s rss_MB rc sigma_ion_H sigma_ion_P network_run_id            stage_E
real14_general  partial 57.24  56.76      549.4  0  0.063062    0.045228    20261005T211623-e9e744f2  True
real14_network  done    28.78  28.29      579.7  0  0.063062    0.045228    20261005T211720-ee4c3d1c  False
lhs00_055       done    4.32   3.99       217.2  0  0.014279    0.011931    20261005T211735-fe3dcdfc  False
lhs00_128       done    2.41   2.09       209.8  0  None        None        20261005T211738-b8c0e661  False
lhsx_007        done    24.48  24.05      569.8  0  0.620602    0.668299    20261005T211746-d473cfb5  False
controls        —       0.71   —          123.2  0
checks 26 · PASS 22 · real-data FAIL 0 · negative-control FAIL 4 (expected pre-fix) · rc 2
A: real14 sha256 = README · general → partial with real Stage E · generation consistent (full_metrics = provenance = Stage E parent = return) · network stop done, no Stage E, stop contract pass · general ↔ network σ (ion 2 modes · e · th) and porosity equal · ε_sphere ≈ 15.639 %
B: lhs00_055 percolating → both modes computed, τ ≠ NOT_COMPUTED · lhs00_128 non-percolating → valid_zero, τ NOT_PERCOLATING · lhsx_007 percolating computed
C (pre-fix, reproduce Codex): C1 ×4 general → done · C1b L1+σ_ratio None general → done · C2 two I/O faults → mixed generation (prov 20261005T211805-fabc336b ≠ fm 20261005T211805-15a459cc) kept=True active=success UI "그대로" · C3 near-hydrostatic → computed vm_cv 100.0 contract v2-invalid-null
Timing: real14 network 28.8 s WSL (73 s here) → 194 batch est. ~15–20 min at 20 lanes.

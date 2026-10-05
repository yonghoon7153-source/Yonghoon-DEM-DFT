# WSL small integration test — POST-FIX (code 11fcf91e8) · 2026-10-05 22:06–22:07 KST · 1저자 WSL ~/dem-audit
ROOT /home/yonghoon71/net_smoke_11fcf91e8_1005_2206 (smoke_report.json · smoke_summary.txt on WSL)
case            status  wall_s pipeline_s rss_MB rc sigma_ion_H sigma_ion_P network_run_id            stage_E
real14_general  partial 54.05  53.53      549.8  0  0.063062    0.045228    20261005T220617-1d567c3b  True
real14_network  done    26.93  26.51      550.7  0  0.063062    0.045228    20261005T220711-68d8163f  False
lhs00_055       done    4.1    3.78       217.5  0  0.014279    0.011931    20261005T220726-76499348  False
lhs00_128       done    2.27   1.96       210.1  0  None        None        20261005T220729-c6a51fe6  False
lhsx_007        done    23.35  22.94      569.8  0  0.620602    0.668299    20261005T220736-408f4e4e  False
controls        —       0.7    —          123.6  0
checks 26 · PASS 26 · real-data FAIL 0 · negative-control FAIL 0 · rc 0
A/B: same 22 checks as pre-fix — all PASS (real14 sha256 = README · general partial with real Stage E · generation consistent · network stop done · general ↔ network σ and porosity equal · ε_sphere ≈ 15.639 % · lhs00_055 percolating computed · lhs00_128 non-percolating valid_zero / NOT_PERCOLATING · lhsx_007 computed)
C (post-fix): C1 general σ_ratio ×4 → failed ✓ · C1b general L1 + σ_ratio None → failed ✓ · C2 two I/O faults → rollback-failure state, not "previous generation kept" ✓ · C3 near-hydrostatic VM pair → CV 0 ✓
σ values identical to the pre-fix run (05fbf15aa) for all five real cases (fixes do not touch the solve).

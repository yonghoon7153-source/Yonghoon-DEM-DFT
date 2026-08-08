# ORCA structure audit summary

The source calculations were rechecked on 2026-08-08 in WSL `Ubuntu-24.04` with ORCA 6.1.1. This was a verification of the completed 2026-07-15 outputs, not a second optimization.

| Fragment | Formula | Method | Final energy (Eh) | Optimization | Termination |
|---|---:|---|---:|---|---|
| H-capped dimer | C₄H₂F₈ | r2SCAN-3c Opt TightSCF | -952.346331900971 | converged | normal |
| CF₃-capped C10 | C₁₀F₂₂ | r2SCAN-3c Opt TightSCF | -2577.579988053998 | converged | normal |

The final element order and coordinates were compared with the repository canonical structures and had a maximum absolute coordinate difference of `0.000e+00 Å` for both fragments.

Repository lineage:

- dimer canonical XYZ: `db/structures/ptfe_dimer_c4h2f8_r2scan3c.xyz`, introduced by commit `5f5ebd33a0d101a601b6a437443824660d7b3010`
- C10 canonical XYZ: `db/structures/ptfe_c10f22_r2scan3c.xyz`, introduced by commit `4d77be9e9f26d1f421fc80c5d96cc7f65c19b6ca`
- package copies: `inputs/ptfe_dimer_c4h2f8.xyz` and `inputs/ptfe_c10f22.xyz`; their enforced hashes are in `PROVENANCE.md`

The raw ORCA outputs are not bundled in this lightweight Gabia input package. Keep them with the final scientific archive if the ORCA optimization itself must be independently audited. Neither job included a frequency calculation, so zero imaginary modes were not established.

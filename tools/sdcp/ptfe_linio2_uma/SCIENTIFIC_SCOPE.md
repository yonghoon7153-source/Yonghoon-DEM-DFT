# Scientific scope and interpretation boundary

## What this package can support

- Generate and quarantine candidate PTFE/LiNiO₂ contact geometries for later manual basin audit and DFT reranking.
- Compare pose scores only within one fragment, one UMA model/task, one cell, and one constraint protocol.
- Record post-relaxation F-Li/F-Ni/F-O distances, multi-F registry, convergence, and periodic-image clearance.
- Preserve diversity across seven representative starting registries and three image-safe orientations instead of promoting a single MLIP minimum. This is not an exhaustive symmetry-orbit site enumeration.

## What the UMA stage cannot support by itself

- Citable adsorption or binding energies.
- Intrinsic Li-site versus Ni-site preference.
- A quantitative comparison of dimer and C10 adhesion.
- Infinite-chain PTFE adhesion, desorption free energy, or finite-temperature coverage effects.
- Charge transfer, Ni oxidation/magnetic-state selection, Li extraction, C-F cleavage, LiF formation, reaction energy, or barrier.

The limitation is model-physics mismatch, not just numerical noise. The legacy `oc20` task is a surface model without dispersion and excludes oxides; `omat` covers inorganic materials but also lacks dispersion and does not let this workflow select the Ni magnetic state. Newer `oc22`/`oc25` heads improve different axes only when UMA-1.2 is actually installed. Use the union of structurally distinct candidates across available heads; no UMA score replaces DFT+U+D3 electronic-state validation for this system. See the official [UMA model/task documentation](https://fair-chem.github.io/uma/).

## Fragment caveats

- `C4H2F8` is H-capped. Any H-dominated contact is an artificial end-cap result.
- `C10F22` is a finite CF₃-capped perfluoroalkane, not infinite PTFE.
- The two models have different cap chemistry, so they do not form a chain-length convergence series.
- Both ORCA structures are optimized singlets, but no frequency job has established zero imaginary modes.

## Cell caveat

The first screen uses the 192-atom 1x4 slab and only three image-safe C10 azimuths. It is therefore a fixed-coverage, fixed-axis screen. A doubled short cell axis is required before claiming an unbiased in-plane orientation search.

## DFT handoff criterion

Pass multiple manually confirmed, structurally distinct basins to DFT-D3. Automated basin labels are contact/orientation/height/RMSD diagnostics only, so the package preserves every eligible relaxed shortlist candidate for manual audit. The handoff also forces a same-azimuth/same-roll Li-top versus Ni-top rigid counterfactual pair for each fragment, so a missing Ni-relaxed UMA pose cannot silently remove the comparison axis. Use the same cell, k-mesh, bottom-half-fixed/top-half-free constraint, one-sided slab dipole correction (`LDIPOL=.TRUE.; IDIPOL=3`), U/dispersion convention, and multiple Ni magnetic starts. Every retained competitor must receive the same relaxation protocol. A preference is defensible only when DFT-relaxed basins remain distinct and their energy gap exceeds the combined magnetic-start spread, k-point shift, U/dispersion sensitivity, and an approximately 30 meV practical floor. For a citable adsorption energy, add a clean slab and isolated fragment computed with the matching reference protocol; those references cancel only when reranking poses of the same fragment.

## Implemented VASP validation scope

`vasp_stage.py` and `vasp_run.sh` implement the fixed-protocol validation after the UMA
handoff. The all-candidate mode preserves 20 relaxed candidates and four matched
counterfactuals when all 20 pass; otherwise it preserves every eligible relaxed candidate
(at least three per fragment). It uses two documented magnetic initializations per surface structure and adds
clean-slab and PAW-PBE+D3 gas references. It reclassifies Li/Ni registry from the final
DFT CONTCAR as Li/Ni/O/mixed/other, blocks reactive/detached/cap-dominated structures,
quarantines top-layer extraction/reconstruction relative to the matching clean slab, and performs a dynamic
2x3x1 to 3x4x1 check.

Even a numerical pass is conditional on the 1x4 fixed-coverage cell and the
PBE+U(Ni=6.2 eV)+D3 protocol. It remains `MANUAL_MAGNETIC_AUDIT_REQUIRED` until local
Ni moments and LDAU occupation matrices are inspected. A method-independent claim
additionally needs U, dispersion, coverage, and slab-thickness sensitivity checks.

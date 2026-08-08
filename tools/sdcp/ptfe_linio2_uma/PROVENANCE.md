# Input and method provenance

## Structures

Hashes below are SHA-256 of the LF-normalized package files and are enforced by `scan.py`.

| Package input | Composition | SHA-256 | Lineage |
|---|---:|---|---|
| `inputs/linio2_104_1x4_relaxed.vasp` | Li₄₈Ni₄₈O₉₆ | `26a48473060243fef55e86d151050b6a27d6e65801b4d3ccd818678913aee25e` | copy of `db/structures/linio2_104_sym_1x4L4_relaxed.vasp` |
| `inputs/ptfe_dimer_c4h2f8.xyz` | C₄H₂F₈ | `dcc0f678202ced02c222cded61a0892a78f177ad12dbb107839bc462ea3bdb7b` | ORCA 6.1.1 r2SCAN-3c optimized structure |
| `inputs/ptfe_c10f22.xyz` | C₁₀F₂₂ | `66dd0bcc4badd26d6db42cc3ed429fbd9ec50a0d467f76a07d2532329efc2d57` | ORCA 6.1.1 r2SCAN-3c optimized structure |

The ORCA structures and outputs were verified again on 2026-08-08; the energies matched the archived 2026-07-15 values and the repository coordinates remained identical. The self-contained verification ledger is `ORCA_AUDIT_SUMMARY.md`. It explicitly records that the 2026-07-15 outputs were rechecked, not recomputed a second time. Raw ORCA outputs are intentionally not part of this lightweight Gabia package.

## Slab lineage warning

This package uses the current 192-atom operational LiNiO₂(104) slab. It does **not** use the retired 96-atom `reference_dft_v2`/`sdcp_phaseB_*` lineage. The tracked slab is the present execution baseline, but its raw DFT relaxation output and every replica-residual audit artifact are not bundled here; do not describe it as fully provenance-closed beyond the repository record.

## Calculation identity

Defaults:

- model: `uma-s-1p1`
- task: `oc20`
- device: CUDA GPU 0
- slab: all 192 atoms fixed
- adsorbate optimizer: ASE FIRE, `fmax=0.05 eV/Å`, at most 200 steps
- initial lower-envelope gap: 2.9 Å above the slab top
- model cache: offline (`HF_HUB_OFFLINE=1`, forced by `run.sh`)

Every result record stores model, task, host, Python/NumPy/ASE/PyTorch/fairchem versions, input and code hashes, the resolved package commit, a model-cache content/symlink identity, a protocol fingerprint, pose parameters, output-structure hashes, geometric gates, convergence, and the warning that the score is not a binding energy.

The Gabia extraction instructions pin the fetched package to one resolved Git commit, write it to `PACKAGE_COMMIT.txt`, and place the short commit in the output-directory name. `run.sh` exports that commit into every protocol fingerprint so outputs from different package revisions cannot be resumed together.

The UMA search and DFT handoff intentionally use different constraint masks. UMA freezes all 192 slab atoms to isolate the adsorbate pose funnel. Handoff POSCARs are regenerated with the bottom half of the slab fixed and the top half plus PTFE free; the exact fixed count and z-cut are recorded per candidate. Handoff atoms are grouped as `Li Ni O C F H`, and the manifest translates nearest Li/Ni/F contacts to the reordered VASP 1-based indices. These are candidate inputs, not jobs that may be submitted without manual structure/mask review.

`oc20` is the compatibility default because it is already present in the established Gabia workflow, not because it is physically complete for PTFE/LiNiO₂. It lacks both oxide coverage and dispersion. A per-head result is an OOD candidate list; later screening must preserve the union of structurally distinct basins across available heads before DFT.

## VASP stage identity

`vasp_stage.py` consumes only a gate-passed `DFT_HANDOFF.json` and hash-matching handoff
POSCARs. It expands every surface cell to a common 34.6 Å c vector without moving
Cartesian atoms, regenerates a 96-fixed/96-free slab mask, and groups species as
`Li Ni O C F H`. Generated VASP packages copy the complete upstream handoff ledger as
`UPSTREAM_DFT_HANDOFF.json`, preserve its full XYZ/POSCAR hashes and package commit,
and carry their own `VASP_INPUT_MANIFEST.sha256`.

The fixed electronic protocol is PAW-PBE, `ENCUT=520 eV`, Dudarev
`U_eff(Ni)=6.2 eV`, `IVDW=11`, `LASPH=.TRUE.`, `LREAL=.FALSE.`, and dipole
correction. Surface systems use 2x3x1 followed by selected 3x4x1 static checks; gas
fragments use Gamma-only boxes. Every surface structure receives the canonical QE
Ni1/Ni2 12-Ni sign pattern repeated across the 1x4 slab (24+/24-) and a net-2
ferrimagnetic magnitude perturbation of that same sign topology. ORCA total energies are never used
as VASP reference energies.

The runner preserves `relax/CONTCAR -> static/POSCAR`, reuses same-mesh WAVECAR/CHGCAR,
and uses only CHGCAR with `ISTART=0` for a changed dense mesh. The analyzer reads final
CONTCARs, not starting labels, to assign Li/Ni registry. A fixed-protocol numerical pass
is still conditional on manual Ni moment/occupation audit and does not close U,
dispersion, coverage, or slab-thickness sensitivity.

Before each phase the runner records the actual POTCAR content hash and TITEL sequence,
host, launch command, NCORE, inherited WAVECAR/CHGCAR input hashes, and the generated
package-manifest hash in `RUNTIME_METADATA.txt`. POTCAR content itself is licensed and
is never returned. Analysis independently checks OUTCAR `SYSTEM`, `NIONS`, `NKPTS`,
`IVDW`, and surface `LDAUU` against the immutable job plan.

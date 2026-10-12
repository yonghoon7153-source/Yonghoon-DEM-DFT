# Independent code-scaling probe, 2026-10-13

Pinned source: `46cd0bdb872e7d6c85ca50ec4172e98377253130`. Source export was read only. Probe: `../probes/code_scaling.py`; machine evidence: `../evidence/code_scaling.json`. No DEM, production network, source edit, or publication was run. The export is not a Git checkout; `git status`/`git worktree list` reported that fact. `source/AGENTS.md` was read; the review artifacts are outside the source tree.

Follow-up temporal check: the actual-run solver file retrieved at `0801d4ceb540f5a5813761b20a5e0f304ed80a03` is byte-identical to this tested solver (same full SHA-256). See `composition_basis.md` and `composition_basis.json`. This verifies the solver-file linkage, not all dependencies or original inputs.

## Q1: absolute baseline conductivity

For a fixed graph, geometry, type map, relative-conductivity law, contact model, and numerical environment, **yes, the computed dimensional electronic conductivity is mathematically proportional to the positive baseline** `SIGMA_AM_ELECTRONIC`. The production call passes it as `run_decomposition(..., sigma_bulk=SIGMA_AM_ELECTRONIC)` at `network_conductivity.py:1723`; that argument is not supplied to `build_network` or `solve_network`. Edge resistances use the relative factors only (`:647–658`, `:676–717`). The normalized solve produces `q = G*L/A` (`:1222`). Publication multiplies the raw `q` by `sigma_bulk*1000` and rounds to six decimals in mS/cm (`:1603–1608`). Certificates also record the baseline.

Thus 0.05 to 0.0041 S/cm is exactly the mathematical multiplier **0.082** (a 91.8% decrease), separately for FULL, bulk-only/contact-free, constriction-only, Hertz, and Physics whenever those branches have a numerical result. It does not change normalized `q`, voltages, current paths, topology, constriction power fraction, or solver status. It is not the sum of the two effective conductivities: the FULL circuit contains `R_bulk + R_constriction` on every edge.

The actual probe uses 15 spheres (3 columns by 5 levels), 22 edges, equal radii 4.5 µm, exact sphere-intersection discs, and three bottom/three top nodes with boundary rule L0. AM_P and AM_S deliberately share a radius here to isolate the conductivity/type correction. Three type assignments (pure PC, pure SC, mixed) were run with both contact modes and both baselines. The actual imported `build_network`, `solve_network`, `run_decomposition`, and `_run_all_networks` functions were used. The production wrapper check adds an independent SE replica to supply its ionic parent record.

All 18 primary branch comparisons have identical floating-point `q`, edges, fields, solve records, and certificates except `sigma_bulk_S_cm`. Largest floating multiplication relative error is 2.04e-16. Six-decimal publication is not literally exact scaling: largest `published_new - 0.082*published_old` magnitude is 5.04e-7 mS/cm, within `0.5e-6*(1+0.082) = 5.41e-7` from two rounds. Use raw `q` (or certificate `I_bottom/ΔV*L/A`) when generating a rescaled sensitivity table; do not promise bitwise scaling of rounded CSV values.

The mixed FULL production-wrapper values are:

| Mode | 0.05 S/cm baseline, mS/cm | 0.0041 S/cm baseline, mS/cm | Normalized q |
|---|---:|---:|---|
| Hertz | 0.663872 | 0.054437 | bitwise unchanged |
| Physics | 0.817986 | 0.067075 | bitwise unchanged |

These numbers demonstrate the code relation, not a material prediction or a fit to the user's real bed.

## Q2: disabling the relative PC correction

The code's law is `f_P(r)=1/(1+(max(r,0.1)/2)^1.5)`, while AM_S has `f_S=1` (`network_conductivity.py:248–262`). At r=4.5 µm, `(4.5/2)^1.5 = 27/8`, so **f=8/35=0.22857142857142856**, and disabling it gives the mathematical factor **35/8=4.375** in a monodisperse all-PC network with positive ordinary edges. Dividing by rounded 0.229 gives 4.366812227, 0.187149% too low. “Divide by 0.229 exactly” is false even in that favorable special case.

Probe conductivity ratios (relative disabled / original):

| Geometry/type assignment | FULL Hertz | FULL Physics | Bulk-only | Constriction-only |
|---|---:|---:|---:|---:|
| Pure PC, all r=4.5 | 4.375000000000013 | 4.374999999999989 | 4.375000000000005 | 4.375 within 1.2e-14 |
| Pure SC | 1 | 1 | 1 | 1 |
| Mixed PC/SC, equal r=4.5 | 3.154656902 | 3.124849017 | 2.384829644 | 3.288178778 |

The mixed case is not a uniform material rescale. For equal radii, disabled/original edge bulk resistances are `f`, `2f/(1+f)=16/43`, and `1` for P–P, P–S, and S–S respectively. The contact law uses the **minimum** endpoint factor, so its corresponding edge ratios are `f`, `f`, and `1`. Full edge ratios consequently differ again. Node voltages change by up to 0.1981 (1 V imposed difference) in the mixed test. Neither volume-average f nor a global `/0.229` recovers the changed circuit. Polydisperse all-PC beds likewise do not have a common f and normally require reassembly and a solve.

The minimum rule is symmetric under swapping endpoint IDs but treats every P–S constriction as the lower-conductivity side. This is a model choice; the static scaling result does not validate its physical accuracy. It is not the ordinary two-halfspace sum `(rho_i+rho_j)/(4a)`. For equal radius PC/SC at 4.5 µm, the code's resistance is 70/43≈1.6279 times that sum. This comparison is an algebraic model distinction, not a recommendation to change the contact law without separate validation.

## Floors, guards, and applicability

- The global baseline is absent from the AM radius floor, exponent, geometry/area branches, min-conductivity rule, ψ computation, ψ floor, and normalized-q guard. For the stated positive .05/.0041 baselines those decisions stay unchanged. There is no global-baseline-dependent exponent clipping in this path.
- Current generation-2 **AM–AM Physics area uses the supplied native contact disc**: `plastic_coverage.py:622–623` returns `native_unsupported_pair`. It does not apply the SE plastic/Tabor material-area model to AM–AM contacts. Physics still changes the constriction resistance through ψ multiplication; Hertz H0 uses Maxwell. All 22 edges in every ordinary test recorded `native_unsupported_pair`.
- ψ = `(max(1-a_eff/r_min,0))^1.5`; at ψ≤1e-4 the constriction resistance becomes zero. A synthetic contact-disc stress at `a/r=.999` triggered 22 floor-only edges: FULL and CF remain computed and scale by the global baseline, while constriction-only is `not_computed / zero_resistance_requires_contraction` at both baselines. Scaling cannot manufacture a value for a rejected branch.
- Disabling f can cross the normalized q>1.5 guard, unlike changing the global baseline. A deliberately undersized synthetic box made the original FULL computed but disabled-f FULL withheld, while CF/constriction diagnostic branches can become `model_over_conduction`. This is a defensive branch test with deliberately invalid geometry, not a physical counterexample. The detailed certificate retains `over_conduction_guard`; the decomposition's high-level reason is `solve_failed`.
- Degenerate zero-area contacts get fixed `R_Maxwell=1e12`, independent of f (`:677`), and nonpositive bulk gets a `1e-12` solver floor (`:1012`). These numerical fallback constants break the simple all-PC disable-factor proof. A synthetic zero-area/positive-overlap PC fixture had FULL and constriction-only disable ratios approximately 1, while bulk-only remained 4.375. Such sentinel-driven tiny results can round to numeric zero despite computed status. Do not use them as physical predictions.
- The all-PC identity therefore presumes a common f, ordinary positive finite resistances, compatible branch availability, and no clipping/guard or sentinel interaction. Global readout scaling is a different and much stronger code identity; even that statement is about finite representable outputs, with existing nulls/zeros/status retained.

## Provenance and output contract

The module file SHA-256 was identical before and after all monkeypatch probes (`da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be`). This establishes read-only source behavior, **not** equivalence of runtime models. A file-based `code_fp` cannot by itself record altered runtime constants or a replaced function. The actual production code-fingerprint function was not included in the source subset inspected by this probe, so this is not a direct test of its implementation.

There is also a concrete consumer restriction. `tau_flux.sigma0_binding_problems` (`:708–745`) compares electronic certificate baseline against the importing consumer's current `SIGMA_AM_ELECTRONIC`. Both .0041 test outputs passed while that constant was patched; after restoring .05, all three electronic certificates were rejected. The constant and emitted certificate cannot be silently changed independently of the consumer contract.

Recommended sensitivity output is a **separate, explicit variant**, carrying source pin/file hashes, input/geometry hash, `sigma_AM_baseline_S_cm`, relative-law name (`pc_radius_corpus_fit` or `disabled`), r0, beta, type-map semantics, contact/min rule, area/bulk/ψ generation tags, solver versions, and branch q/dimensional values/status/certificates. Retain the frozen published baseline and its manifest. A readout-only .0041 variant can reuse raw q but must declare its changed baseline; disabled-f mixed/variable-radius variants require a fresh network solve. Do not label a patched model as the same calibrated model merely because source files and file fingerprints are unchanged.

Reproduce from the workspace with bundled Python and `-B`, running `ps45_sigmae_review_20261013/probes/code_scaling.py`; it prints JSON. Dependencies are read from the existing local review dependency folders. Every monkeypatch is restored in `finally`.

# Independent G2/G3 review — 2026-10-05

Reviewed pin `30c8205c5efb3873ae6fa856881fa184bd041d4d`. No production edits or campaigns. Small CPU synthetic tests only. All line references below refer to this pinned snapshot, except explicitly linked upstream primary sources.

## Verdict

- **G2 HOLD** for the producer's invalid-input/zero-normalization gates (G23-01). The branch tensor, force orientation and symmetric-part VM mathematics are sound for the stated particle-contact-only descriptor. This is not evidence that real14 or the 194 beds contain malformed geometry.
- **G3 GO for the added physical-edge power-share statistic and neutral boundary extraction**, with the scope qualifications below. Integration with the new G5 stage-success contract is **HOLD**: an actual disconnected producer reports `sigma_full_status=not_computed`, not the mock's `valid_zero`. Parent review owns that combined finding.
- Real14 numbers were **not independently replayed**: both pinned compressed input fixtures were unavailable through the connector. The stress regression reached 37/38 executed assertions; only the real14 group was unavailable. Its exception handler adds one failed placeholder in place of five expanded real14 assertions (L12, L12b–e), so the available tests do not establish the claimed 42/42 replay. Do not treat fixture unavailability as a source regression.

## G23-01 — P2: input-validation failures can be published as OK and false zeros

Location: [dem_analysis_core.py:1274](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1274), contact-only finite check [1289](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1289), summary [1349](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1349), mesh predicate [1361](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1361).

The function checks finiteness of contact F/cp/(Fn+Ft), not atom positions, radii, volumes or plate height. A single isolated particle with radius NaN disables the all-atoms c_strs comparison and enters the population as an undefined stress. Since `NaN > 0` is false, the summary emits CV=0 and all phase ratios=0, then returns OK. This is not just a hypothetical foreign caller: the replay loads the malformed row using actual `analyze_contacts.load_atoms_raw` ([line 24](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/analyze_contacts.py:24)) from the owned three-row CSV. Results:

- Valid AM_P particles each have VM 0.2148591731740587.
- The isolated SE particle has VM NaN.
- Producer: `status=OK`, `vm_cv=0.0`, AM_P mean 0.2148591731740587 but ratio 0.0, SE mean NaN and ratio 0.0.
- Separately, plate_z=NaN with source=mesh returns OK, `plate_flag=mesh`, zero plate contacts and available nowall summaries.

Two normalization edge cases also contradict the declared checking contract:

- [1293–1294](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1293): total F=0 but Fn+Ft=(0,0,-1) reports decomposition error 0 and OK when c_strs is absent. Zero total force must not bypass a nonzero discrepancy.
- [1320–1321](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1320): correctly matched all-zero c_strs and contact force produce an infinite virial mismatch and FAILED, although both totals are exactly zero.

Minimum fix: reject nonfinite positions/radii and nonpositive radii/volumes before tensor construction; validate finite, physically valid periodic lengths and plate height when used; never summarize a nonfinite tensor/VM population as zero. Use explicit zero/absolute-plus-relative residual handling for F decomposition and virial comparison. Keep failed values absent and propagate reasons. Add regressions for all four cases; define any truly zero-load CV/ratio convention separately from invalid data.

Replay: [probe_lw_independent.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/probe_lw_independent.py), [actual CSV input](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/atoms_nan_radius.csv), [stdout](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/probe_lw_independent.parser.stdout.txt). All assertions reproduce the current defects (exit 0 means reproduction success, not production correctness).

## G23-02 — validation limitation: a global diagonal virial check is not proof of matching frames

Location: claimed scope [dem_analysis_core.py:1255](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1255), implemented gate [1316](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1316).

Independent example: four unit-radius atoms form two equal-geometry dimers (separation 1.8), one AM_P dimer and one SE dimer. Atom c_strs records forces 1 and 3. Swap those two forces in the contact input while retaining correct ids, finite contact points, and F=Fn+Ft. Both correct and mismatched cases return OK, branch/r=0.9, and virial residual 1.23e-16. The AM_P ratio changes from 0.5 to 1.5; SE changes from 1.5 to 0.5. CV remains 50%.

The sum check is mathematically useful and catches global sign/scale errors; it discards spatial and phase allocation. This does **not** establish that any supplied bed is mispaired. It does falsify a blanket claim that passing this gate establishes the two dumps' frame correspondence.

Minimum safe wording: “global diagonal virial consistency check,” not frame verification. Retain and validate atom/contact timestep and file provenance. If stronger numerical pairing detection is required, independently reconstruct the *old 50/50 per-atom virial* from contact forces and compare per-particle residuals (with output-rounding/time-evaluation tolerance). Do not directly compare per-particle LW and c_strs: they intentionally use different partitions.

The upstream output compute itself performs another force evaluation, so bitwise force agreement with the integration-stage virial is not generally a defensible tolerance requirement. [LIGGGHTS compute documentation](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/master/doc/compute_pair_gran_local.txt).

## Q3 — what is physically supported

The reviewed implementation adds b1⊗F to id1 and b2⊗(-F) to id2 ([core:1313](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/dem_analysis_core.py:1313)); compression is negative with center-to-contact branches. Upstream `cpl_add_pair` passes `i_forces.delta_F` and (i,j), independently supporting the assumed id1 orientation. [Primary pair_gran.cpp](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/pair_gran.cpp).

Upstream uses center difference x_i−x_j with F_i in the virial and partitions that pair virial equally between atoms, then negates it for stress units. Thus the new branch partition differs legitimately from the old 50/50 atom attribution. [Primary pair_gran_base.h](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/pair_gran_base.h), [pair.cpp](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/pair.cpp), [compute_stress_atom.cpp](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/compute_stress_atom.cpp).

The spherical upstream contactPoint is the radius-weighted point between centers, not precisely the equal-overlap midpoint described by one handwritten unequal-radius test comment. Production reads the supplied cp, so that comment does not create a production tensor error. [Primary compute_pair_gran_local.cpp](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/compute_pair_gran_local.cpp).

The x/y minimum-image operation and symmetrized full-tensor VM formula pass explicit periodic/tangential/manual tests. Tensor transpose convention cannot change the symmetric VM or Frobenius asymmetry diagnostic. The scalar is a **symmetric particle-contact stress descriptor**, not complete dynamic/couple/kinetic/wall stress. A median asymmetry statistic does not establish rotational equilibrium for every particle.

Wall exclusion masks are correct for the explicitly assumed horizontal floor at 0, flat mesh plate at plate_z, and periodic x/y; the routine does not verify those assumptions from the DEM deck. Excluding wall-touching particles produces a selected-population statistic, not a correction of the full bed's missing wall forces. The upstream pair compute is separate from the mesh-wall compute; its wall variant also excludes primitive walls. [Primary compute documentation](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/master/doc/compute_pair_gran_local.txt). Exact actual DEM binary/deck provenance was not established by the upstream-master inspection.

## Q4 — power share and disconnected-state producer evidence

The FULL call is used at [network_conductivity.py:1156](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:1156). Field records contain physical edges only ([922](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:922)); the new routine correctly sums I²Rc / I²Rtotal ([979](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:979)). A finite positive-resistance physical network gives a dimensionless value in [0,1]. This is not the old unweighted mean of edge resistance fractions. Virtual electrode heat is absent from numerator and denominator, as intended.

Independent two-path circuit: physical (Rb,Rc)=(1,9) and (1,0), distinct bottom/top nodes. Analytic share including the solver's finite electrode conductance is 0.0916787133551442; actual result is 0.09167871335514417. Physical heat 0.9094044479454131 + electrode heat 0.06007501223551508 equals unit-current input power 0.9694794601809258.

Nonblocking qualification: electrode exclusion does not remove electrode influence on the solved currents. The same circuit's ideal-electrode limit is 9/110=0.08181818181818182 (12.05% smaller relative to that limit). The C1c test title's general boundary-independence claim ([test line 74](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/test_constriction_power_share.py:74)) is too broad; its shared-terminal fixture cannot test this. Label the metric conditional on the actual FULL boundary solution; any electrode-sensitivity diagnostic is an additional design choice.

Actual broken 21-node L0 chain: no spanning component gives `sigma_full=None`, `sigma_full_status=not_computed`, percolating_fraction=0 and power-share=None with no-percolating-FULL reason. None is appropriate for the undefined 0/0 power *share*. The **conductivity** state is the separate G5 contract issue; do not “fix” the undefined share by giving it zero. Relevant producer exits [589](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:589), status mapping [94](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:94), output [1226](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:1226).

Replay: [probe_network_independent.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/probe_network_independent.py), [stdout](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/probe_network_independent.stdout.txt).

## Q5 — boundary extraction and the GOLD claim

Inspection found no change in the old L0→L1→L2 set selection. L0 uses each particle's radius; recorded L0 width uses the global target-particle r_max as an upper-bound diagnostic, not the actual thickness of one uniform slab. L1 uses plate fractions; L2 uses observed-z fractions. See [network_conductivity.py:187](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/network_conductivity.py:187).

“GOLD 8” means **eight assertions**, not eight independent beds. The stored numerical GOLD comprises three chain fixtures × two contact modes, compared after output rounding to eight decimals ([test:53](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/test_network_boundary_rule.py:53), [test:88](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/source/scripts/test_network_boundary_rule.py:88)). Equality of these rounded values does not itself prove raw bitwise numerical equality.

I independently fetched the stated pre-extraction source `eedada5d3` (Git blob `2e0c4a47721cd8593b039fe1e189419bbb2eea64`). Its solve_network function AST is identical to the new one. Direct old/new builds produce identical boundary sets and raw float.hex conductance/sigma outputs in **18/18** comparisons: L0/L1/L2 × hertzian/physics × full/bulk_only/constriction_only; old field-disabled versus new FULL-field-enabled route is covered. This supports extraction neutrality for those cases, not physical validation or a campaign-wide numerical guarantee.

## Replay inventory and provenance

Use [test_run_metadata.final.json](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/test_run_metadata.final.json) for exact Python/environment and script commands. Run from the review root. PYTHONUTF8=1 and PYTHONDONTWRITEBYTECODE=1. Dependency search order keeps the Sept30 numpy/scipy environment first; plotting dependencies follow it, with MPLCONFIGDIR confined to this evidence directory.

| Replay | Result |
|---|---|
| test_love_weber_stress | 37/38; real14 compressed input unavailable |
| test_constriction_power_share | 16/16 |
| test_network_boundary_rule | 8/8 |
| lhs_stress_constriction_audit --selftest | 9 PASS |
| webapp test_stress_lw_labels | 33/33 |
| webapp test_constriction_power_labels | 21/21 |
| independent network probe | all assertions, including 18 raw old/new comparisons |
| independent LW probe | all falsification assertions reproduced |

The initial stdout files preserve earlier missing-dependency attempts; use the metadata's final stdout filenames for completed replays.

Newly fetched source dependencies, mesh text and historical module all match their connector Git blobs; [hash evidence](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g1_lhs_network_review_20261005/evidence_g23/dependency_blob_verification.stdout.txt). The atom/contact gz paths returned empty content even with explicit base64 encoding; direct blob fetching refused non-UTF8 content. Expected blobs: atom `ee206e15b9ff9457d0547d099c9249054b7171d2`, contact `a3e41f709cce79a5ef5e058d6bb8d39cd9c3ff81`. No placeholder binary was written and no unpinned fixture substituted.

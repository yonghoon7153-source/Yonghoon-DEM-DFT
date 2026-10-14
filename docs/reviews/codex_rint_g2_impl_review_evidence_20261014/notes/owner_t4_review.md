# Owner/CNC and T4 independent review notes

Pin: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`. Source snapshot read only. Probes used Python 3.12 on Windows, NumPy/SciPy versions recorded in `evidence/owner_independent.json`; all numerical threads set to one, bytecode disabled. Windows `resource` was shimmed only for peak-memory telemetry (`ru_maxrss=NaN`); no raster, owner, census, or solver numeric function was changed except a direct sparse solve on the 1,072-DOF mismatch fixture.

## New actionable issue: bind the contact plan to solver voxel spacing (P2)

Location: `scripts/step3_sigma.py:1841–1842` (guard call), `:1597`, `:1616–1617` (guard checks sid bytes but has no spacing argument); consequence at `:2009` (uses solver `vox` with the plan's already normalized `rface`). `am_iface_plan` does retain `vox` at `:1486`, but the solve never compares it.

A normal, unmodified plan built at h=0.2 µm can be passed to `solve_sigma_z` with the same sid array at h=0.4 µm. The guard accepts it, solves, and publishes the original contact geometry and G summary, although each face has four times the physical area. This is an E5 physical-grid binding gap, independent of the known hold on quantitative adoption. No mutable dictionary edit is needed.

Evidence: `probes/owner_vox_mismatch.py` → `evidence/owner_vox_mismatch.json`.

- Two AM_S spheres R=1 µm at z=1 and 2.98 µm, h=0.2, r=1e-3 Ω·cm², sid shape 10×10×20, 16 film rows, 1,072 DOF.
- Original plan: A=0.06251769380643697 µm², reported pure-film G=6.251769380643698e-7 S.
- Mismatched solve at h=0.4: accepted with empty rejections; `cg_info=0`, residual 2.6821546712579842e-15; actual pure-film G obtained from the assembled face r values and solver face area is 2.5007077522574787e-6 S, exactly 4 times the recorded value. Result still reports `vox_um=0.2` and the old A.
- A legitimately rebuilt plan with c, r and h each scaled by two produces exactly the same sigma, 0.0021331551689598217 S/cm, but correctly records A and G four times larger. Thus the mismatched call silently solves the scaled geometry while certifying the original plan geometry; this is not merely an expected conductivity difference between valid rescalings.
- Minimum fix: pass solver spacing to the plan guard and reject a spacing mismatch before assembly. Add a negative test using an unchanged sid and unchanged plan but different solve spacing. Verify a rebuilt scale-consistent plan remains accepted.

## Independent checks that passed

Evidence: `probes/owner_independent.py` → `evidence/owner_independent.json`.

- RINTV-01 contract epsilon counterexample: all six permutations select canonical owner 1, epsilon-band size 2. Independent set-min oracle: 550 random cases (2–12 claimants), no mismatch.
- Frozen-mask owner/contact/face/canonical-particle invariance: six independent four-sphere overlapping geometries, all 24 permutations each, no mismatch. These include 46–112 cells with three or more claimants. Independent power/min-band recomputation on their exposed candidate sets matches every owner.
- Prior RINTV-02 boundary fixture reproduces 3,170 versus 3,171 AM cells, exactly the changed cell (15,15,15), sid 0 versus 2. Diagnostic reports matching claimant geometry, unequal masks, and `owner_judged=False`. Freezing the 3,171-cell mask yields identical owners/faces/contacts in both orders and no unclaimed-mask rejection.
- Reproduced all three beds at h=0.4: census class counts, low-resolution counts, unregistered faces/pairs, seam counts, no-support counts, AM mask fingerprints, and DEM crosschecks match. Tiny percentile differences across environments only: case15 contact p10 1.7200596267485022 versus 1.7200596267485038; kit contact median 5.513162286005207 versus 5.513162286005173; kit ambiguous p10 26.323984938940377 versus 26.323984938937947.
- Reproduced all seven registered raw raster permutations for all three h=0.4 beds. Entire `ref` and per-permutation records match submitted T4-3 JSON exactly (sid, labels, masks, location, lens kind, pid differences, sample cells). No large-grid repeat or realbed sigma campaign was performed.

## Q6: T4-1 and D4′

The census is correct for its declared population and frame. At h=0.4 it reproduces contact/ambiguous/gap counts 563/27/69, 106/3/15, and 3010/91/402, with explicit unavailable additive coverage and assumed kit dump precision. These are useful development frequencies, not evidence of production prevalence under an unverified MPM frame, origin phase, additives, and kit dilation.

The two joined-bed observations support using the actual joined dump to resolve scaffold rounding ambiguity when that provenance is available. They do not establish a universal law that every ambiguous scaffold pair is a DEM contact; preserve per-pair classification. Likewise, zero DEM contacts among the registered gap pairs supports treating their raster necks as artificially created support in these beds. A registered cut policy is a defensible model choice, but the census alone does not certify the physical electrical law, production applicability, or DEM/voxel topology equivalence. The disclosed unregistered faces and 70/10 seam contacts remain relevant to D4′; they are not restored by cutting gaps.

## Q7: T4-3 and D21

The implemented raster quantities match the registration and reproduce exactly at h=0.4. The provided sigma result answers the size question for real14 at h=0.4 under the registered AM-only model, not other grids or production. It is appropriate to report the observed maximum magnitude of 0.338% and the documented file-order direction; it is not a universal error bound.

D21 can be brought to the first author as an explicit design decision because the input-order effect is measured and systematic in that sample. There is no preregistered significance threshold to claim that 0.338% automatically mandates a new bulk generation. Keep the legacy OFF contract until that decision; avoid treating RINTG-11 as production-wide closed. Per-particle pid changes matter separately even where sigma does not change.

## Q9: RINTV-01/02 closure scope

Support `verified` for the implemented epsilon-set owner rule and the corrected frozen-input/raw-diagnostic contract, with the exact scope above and existing regression tests. Zero realbed tie/unclaimed counts are not the proof: synthetic counterexamples and set/permutation tests exercise the mechanism. This does not close T3 numerical/model validation, production representativeness, RINTG-11's remaining grids/additives, or the separate new voxel-spacing binding issue.

## Non-findings

- T4 scripts importing Unix-only `resource` is an execution-environment issue for this Windows review; it does not invalidate the supplied Linux numerical evidence.
- T43's 1,200-second cost check happens after a solve completes (`:133–136`), so it bounds whether further solves begin, not the current solve duration. All supplied solves are well below the threshold; do not elevate this into a result-invalidating defect.
- Owner claim arrays internally follow input particle ordering, but the canonical owner/contact/face results compared by the contract are invariant. No false failure asserted for internal claim-array order.

Run probes from the review workspace with the bundled Python executable and `-B`; no source writes, Git mutations, WSL use, or production runs are required.

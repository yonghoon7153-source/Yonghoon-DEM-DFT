# Independent area / physical-design review

Pinned implementation: `5e0efdb8d`; snapshot HEAD supplied by root: `62f9e4cb3e969d13cf0c311858b5159ac75d6396`.
This is a design review and small CPU arithmetic/FV probes, not production physics output.
No source changes. Reproduction: `probe_area_contract.py`; complete output: `probe_outputs.json`.

## G2: HOLD

The split between film ASR and lumped fiber junction resistance is defensible, but D2/D4/D5 are not yet a closed discretization contract. In particular, contact area normalization is not a repair for the wrong boundary location or the wrong graph topology. Release the design gate after fixing that claim, specifying geometric contact patches and exceptional contacts, and adding nonuniform-potential and junction-limit tests.

## Findings

### P2-A: area normalization does not fix contact placement

Locations: `source/docs/reviews/contact_resistance_pipeline_draft_20261002.md:100`, `source/docs/reviews/codex_rint_stage1_request_20261003.md:84` (the row claiming location is repaired), and `source/scripts/step3_sigma.py:985` / `:1005` (each interface face connects its own pair of FV nodes).

The statement "N faces in parallel = Rc exactly, origin/vox independent" is conditional on equal potentials at all endpoints on each side. It is not generally true in a finite-conductivity FV solution. The algebra only fixes `sum(g_film)=1/Rc`; the dissipated power is `sum(g_film,e * jump_e^2)`, so nonuniform jumps and the interface location remain material.

Independent numeric evidence:

- Three-node resistor graph, same bulk edge and two film edges with `R=2` each: both arrangements have `sum(g_film)=1`, yet moving one film endpoint gives terminal `R=1` versus `22/13=1.69230769` (+69.23%).
- Actual pinned `solve_sigma_z`, identical 15x1x15 conductive grid, conductivity and electrode masks, identical 15 interface faces, identical normalized film conductance. Moving only the pid cut from z=1 to z=14 changes `sigma_ON/sigma_OFF` from `0.5269418141` to `0.7291597217` for `Rc_internal=1`. The effective added resistance is `2.4275649794` versus `1.0044065699`, despite the prescribed value 1.
- Actual pinned `rasterize` and `solve_sigma_z`: two AM spheres, R=1 um, overlap=0.02 um, fixed bridge=0.24 um, same sid geometry and same sigma. Apply contact-area normalization independently to original stamped pid and geometric midpoint labels. Both have exactly `sum(g_film)=6.25176938064e-7 S`. At vox=0.2, normalized ratios are `0.6241260201` and `0.6474454905`; at vox=0.1 they are `0.6755034001` and `0.6999486508`. All solves converge. This is a direct counterexample to the proposed closure, not an estimate of production error.

Minimum safe design: preserve the original pid consumer semantics, but build a separate interface ownership/geometry rule that partitions overlap and bridge voxels at a physically specified contact surface. For equal spheres the center-normal midpoint plane is an obvious test reference; unequal spheres need the geometric intersection/radical plane or another explicitly justified contact plane. Do not assert a broad total-conductance identity in heterogeneous FV. If Rc is intended as a genuinely lumped two-port contact, explicitly model two contact ports and their access coupling; that changes the model and needs validation. Geometry, contact support, film area, and bulk spreading are distinct contracts.

### P2-B: unregistered/gap-contact L1 fallback violates the proposed resolution rule

Locations: draft `:96`, `:103`, `:181`.

The draft forbids L1 for unresolved one-cell fibers/small curves, then assigns unregistered faces to L1. A face created by quantization or a bridged positive gap may be exactly such an unresolved object and has no known physical film area. A label does not supply missing physics. Keeping an unphysical conducting edge also cannot be fixed solely by an area factor.

Minimum safe design: distinguish geometric contacts from optional gap/tunneling bridges. For quantitative contact-film mode, reject unsupported cases or remove their connection according to a preregistered topology rule. A diagnostic legacy-retention arm may retain them, but must use a separately declared conductance model and must not claim DEM-contact-area closure. No automatic L1 fallback for objects outside its validity range. Report unregistered edges by connected physical patch and channel, not only count.

### P2-C: proposed cross-model bounds and equal logarithmic response are not invariants

Locations: draft `:149` and `:150`; network model `source/scripts/network_conductivity.py:401`, `:421`; voxel model `source/scripts/step3_sigma.py:991`.

`sigma_FULL <= sigma_vox <= sigma_CF` is not a proved bound: the models have different nodes, bulk-resistance approximations, junction topology and electrode coupling. Positive resistance gives monotonicity within an unchanged graph and boundary model; it does not order these two different graphs. Even matching the geometric inputs and contact film r/A does not require equal `delta ln sigma`.

Independent counterexample to the response requirement: two valid series models with baseline R=1 and R=10 receive exactly the same film R=1. Their ON/OFF conductivity ratios are 0.5 and 10/11; logarithmic changes are -0.69314718 and -0.09531018. Both film implementations are exact. More generally, the logarithmic response depends on the interface dissipation fraction in each model, which differs when bulk or current paths differ.

Minimum safe design: call FULL/CF comparisons model comparisons or empirical brackets, with no pass/fail sandwich unless a variational or edgewise comparison is established for that fixture. First verify each model against its own analytical/contact reference. Compare absolute and relative changes with a preregistered model-discrepancy budget; do not force agreement by fitting r. Same-graph OFF/ON monotonicity and energy identities are genuine gates. The draft already rightly excludes claiming independent cross-validation for shared inputs.

Additional Q6 biases worth registering: different finite electrode resistances and contact sets; contact-direction/angular multiport interactions lost by one node per particle; periodic image/contact multiplicity; input relative-sigma rules; fiber/carbon paths absent from an AM-only DEM comparison; `Rj` contact counting and subvoxel geometry; `r/sigma` contrast and linear-solver tolerance. Network `:664` also recomputes its finite boundary conductance from the current mode's edge conductances; adding a film can therefore change its numerical boundary resistance unless fixed explicitly for the comparison.

### P2-D: "unresolved contact means no constriction and no double count" is unsupported

Locations: draft `:139`, `:182`, `:183`, with validation draft `:55`.

The existing FV graph has finite half-cell/axial resistances and topology-dependent spreading even when a physical junction is unresolved. Absence of a resolved physical contact does not prove that a measured lumped Rj excludes everything already represented. A simple reference-plane check: leads of 1 ohm each plus a pure contact 5 ohm give total 7 ohm. If the measured terminal value 7 is inserted as Rj while both leads remain, the model gives 9 ohm. The relevant question is the measurement/reference-plane definition, not resolution alone.

Two nodes per crossing cell plus an Rj edge can be consistent, but is not automatically exact. It needs all the following stated before ②:

- Preserve each fiber's membership at crossing cells (a single winning fid cannot reconstruct it). Support k fibers with k local dofs, not only two, and route each axial branch to its own fiber.
- Do not retain the old fused/bulk edge as a parallel bypass around Rj. Define which half-length/axial/access resistances remain, and align those with Rj reference planes and the single-fiber conductivity/diameter convention.
- One physical junction instance, not necessarily one unordered fid pair. The same two fibers may touch at multiple separated places or periodic images. Two true junctions of Rj between equipotential fibers yield Rj/2, not Rj. A pair-wide area normalization can collapse this multiplicity incorrectly. Long parallel contact requires its own extent/counting law.
- Use an edge ledger containing endpoint dofs, physical conductance, physical junction id and resistance components. Assemble `g[[1,-1],[-1,1]]`, derive current `g*(phi_i-phi_j)` and dissipation `g*(delta phi)^2` from exactly that ledger. Include junction edges in connectivity before floating-component pruning (current pruning is voxel-only at `step3_sigma.py:937`).
- Treat Rj=0 by exact contraction of the relevant dofs or another proven limit; merely disabling creation of extra nodes is not sufficient in every overlap geometry. Verify Rj->infinity disconnects inter-fiber transfer while leaving within-fiber transport intact. Test same-cell, adjacent-cell, diagonal and triple crossings, multiple junctions, origin shifts, and fused/zero-junction limit.

Unit reminder confirmed independently: `A_face_cm2 = vox_um^2 * 1e-8`; thus `r_face[ohm cm2]=Rj[ohm]*N*A_face_cm2`. The current FV matrix uses conductance 1e4 times physical S, so a direct Rj edge must use `g_code=1e4/Rj`. For `r_face = r*(N*vox_um^2/Atrue_um2)`, the area ratio is dimensionless and the factors cancel.

## L1 judgment (not a standalone rejection)

Draft `:93-95` is defensible as a local area-quadrature correction in the resolved-interface limit. For normal n, face density on axis k is `|n_k|/h^2`, so `g_film=h^2/(r*sum|n|)` gives formal interface energy `integral jump^2/r dA` when endpoint jumps approximate the same smooth local trace jump. Likewise `r/|n_k|` gives `sum n_k^2=1`. This does not require an entire curved surface to be globally equipotential in the refinement limit.

Neither prescription is an exact finite-grid solution merely because a uniform-jump plane has the right total area. At n=(cos30,sin30), sampled jumps (1,2) give L1 current 1.3660254 versus axis-rule current 1.25, and energies 2.0980762 versus 1.75. This finite-grid inequivalence does not prove either continuum limit is wrong. It demonstrates why the proposed area-count tests are insufficient to select them for a heterogeneous-potential problem. Use manufactured finite-conductivity fields with nonuniform interface jump, heterogeneous material sigma, curvature, translations, and triple points; verify terminal current, local continuity, and energy as h decreases. A fixed 5-cell centroid window and radius/vox>=3 threshold are candidates requiring measured error, not guarantees.

## Direct answers

- Q2: D1 film-only is sound; D2 pair categories are a useful first routing rule but need local geometry validity and explicit exceptions. D3 intersection-disk area is the consistent initial DEM comparison convention, named accurately rather than Hertz; defer physics/Stage-E until LHS-25, per the accepted tau decision. D4 as written is not sufficient. For SE use the transported post-deformation grain geometry and its reconstructed interface measure; do not mix a pre-deformation DEM contact area into that same film law unless explicitly studying a different model.
- Q3: a physically specified interface-ownership/contact-plane rule is needed independently of (b), or an explicitly different port model. A vox ladder is evidence only after physical geometry, bridges, contact ledger, area source, electrode planes and masks, relative origin and normalization, input conductivity convention, and solver tolerances are held consistently; test multiple origins and at least one analytical/reference contact. A stable ratio alone can converge to the wrong geometry and can cancel errors common to ON/OFF.
- Q5: separate fiber membership and an augmented graph are a reasonable architecture. D5/D6 need the ownership, topology, reference-plane, physical units and energy ledger requirements above. Dual nodes alone do not prove exactness or remove double counting.
- Q6: use the comparison to expose model discrepancy, not as a physics truth or an unproved mathematical bound. The listed biases are a useful start but incomplete; see P2-C. Equal r/A is an input agreement, not a guarantee of equal delta ln sigma.

## Reproduction

From review root in PowerShell:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/deps'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' evidence_area/probe_area_contract.py
```

The script imports the pinned solver, runs small CPU fixtures, asserts expected graph identities and converged FV solves, prints JSON, and writes no files. The saved JSON was captured verbatim with apply_patch. The numeric evidence is independent of the supplied review probes.

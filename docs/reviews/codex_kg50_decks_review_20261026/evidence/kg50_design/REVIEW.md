# KG50 design and runtime review: Q3, Q5, Q6, Q7

Review authority: the attached snapshot bytes, claimed commit 3056eef12b60ed754fa59ec5a84fad811b14c9c8 (unpublished, therefore not independently resolved remotely). This is not itself a defect. Baseline physical-law redesign is outside scope. No DEM, MPI, cluster, WSL, SSH, submission, shared Git mutation, or production edit was performed.

Source authority: official CFDEMproject/LIGGGHTS-PUBLIC at commit 3d5c00f20519e6bb6eb6756f51f1ad36564e649d. Twenty-four retrieved source/document files were verified against the Git blob SHA returned by the GitHub connector. See sources/source_manifest.json. The deployed lmp binaries were not inspected and their equivalence to this source remains unverified.

## New actionable findings

### D1 — P1: All four speed fixtures cannot pass insertion with NP28 or NP56

Primary local locations:
- snapshot/repo/scripts/make_se_size_decks.py:556 (explicitly inserts benchmark at NP28/56, merely removes AM count gate).
- snapshot/repo/scripts/make_se_size_decks.py:568 (generates full insertion prefix).
- snapshot/repo/docs/data/kg50_decks_20261026/speed/kg50_spd_d07_b40_sk05_np56/input_kg50_spd_d07_b40_sk05_np56.liggghts:118 (insert/pack, overlapcheck yes, default border guard).
- Same input:38 (AM radius 3 um), :46 (processors * * 1), :129 (99% total gate).
- Same folder/run_kg50_spd_d07_b40_sk05_np56.sh:18 (runs this insertion at NP56).
- README.md:31 (submits all four such fixtures).

The default border rule is a stronger problem than SELF-70 rounding. Pinned fix_insert_pack.cpp:175 sets check_dist_from_subdomain_border_=true; lines 479–488 reject every candidate less than its bounding radius from any subdomain face. domain_I.h:126–143 computes the minimum absolute distance to all six subbox faces, with no exemption for global or periodic faces. The input never overrides this default.

For the square 40 um domain with processors * * 1, the minimum-area grids are:
- NP28: 4 x 7 x 1, cells 10 x 5.7142857 um; maximal distance to the nearest narrow face is only 2.8571429 um.
- NP56: 7 x 8 x 1, cells 5.7142857 x 5 um; maximal distance is 2.5 um.
Both are less than the required AM bounding radius 3 um. Every integer Px*Py=28 or 56 factorization has at least one width <6 um, so this does not depend on choosing one grid orientation.

The number fraction of AM calculated from the actual two-template mass distribution is 0.003033546735. Near-uniform per-rank targets are 11,160.93 and 5,580.46, so the local AM counts have floors 33 and 16. The distribution explicitly wires large particles first (fix_particledistribution_discrete.cpp:463–472). The insertion loop retries the same current particle until success or exhaustion (fix_insert_pack.cpp:465–500). Thus an AM blocks all later SE particles on that rank; increasing maxattempt cannot create an admissible AM center. The normal uniform allocation consequently predicts zero insertion.

Even without assuming exactly uniform Monte Carlo region allocations, an AM-free rank can have at most 329 particles targeted: floor(n*f_AM)=0 requires n<=329. Any rank with an AM inserts none. Therefore an intentionally loose upper bound on all inserted particles is 28*329=9,212 or 56*329=18,424, both far below the 309,380 total-count gate. The speed phase is unreachable under the pinned source semantics.

Implication: these fixtures provide no usable 20,000-step speed measurement. This is a new concrete launch blocker for the proposed speed jobs, not a measured timing or an assertion of a simulated result.

Minimal remedy: generate one composition-gated NP1 insertion checkpoint, then read that same inserted state at each desired NP/skin for the benchmark. This also eliminates independent-insertion composition/configuration changes from the NP comparison. Keep the border guard; disabling it permits cross-rank insertion overlaps and is not an equivalent repair.

Official source links:
- [insert/pack default and rejection loop](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_insert_pack.cpp#L175)
- [all-face distance calculation](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/domain_I.h#L126)
- [large-first distribution list](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_particledistribution_discrete.cpp#L463)

### D2 — P2: The repaired early-settling fixture still cannot select compression NP or certify its ETA/skin behavior

Locations:
- scripts/make_se_size_decks.py:557 claims that early falling gives a lower bound on the small-skin benefit.
- docs/data/kg50_decks_20261026/README.md:58 uses speed results to choose production NP.
- README.md:65–67 ties first measured timing to the 5–7M-step estimate.
- docs/50kg/dem_plan_20261026.md:91 chooses a common production skin after this test.

The fixture ends after 20,000 steps =0.02 s: 10% of the settling phase, and 0.29–0.40% of a 5–7M-step total. It has gravity 98.1, viscous gamma 1e-5, no top mesh, no compression, no atom dumps and no periodic checkpoint beyond the initial checkpoint (next restart is 50k). Intended compression uses gravity 9.81, gamma 0.5 (50,000 times greater), moving mesh, denser contacts, atom/mesh dumps, and 200k checkpoints. No monotonic lower-bound theorem follows from changing these costs together. A falling-phase winner can differ from a dense compression winner; the four timings do not identify the production bottleneck.

The initial SE volume fraction is 0.110077, whereas the README neighbor estimates use about 0.30: the estimated candidate population at 0.35 um radius, skin2 is about 50.5 initially versus137.7 at 0.30, before correlations and excluded volume. A short early timing cannot be multiplied into a production ETA without phase information.

Minimal remedy: retain a corrected early fixture as an explicitly limited diagnostic; for choosing production NP/skin, additionally compare short runs from the same relevant dense compression state with actual mesh, damping, dt and output configuration. Record elapsed step rate, neighbor rebuilds/dangerous builds, neighbor/ghost counts and selected physical diagnostics. This request changes benchmark coverage, not baseline physical law. Until such a comparison exists, mark compression ETA and the assertion that the early speedup is a lower bound as unverified. It need not stop an exploratory diagnostic.

### D3 — P2 decision limitation: Three-seed D3 mean agreement is not a statistical equivalence gate for all SE sizes

Location: docs/data/kg50_decks_20261026/README.md:71; planning rationale at docs/50kg/dem_plan_20261026.md:94.

The exact present rule uses only mean difference against four tolerances and reports SD without incorporating it. A deterministic counterexample using its own planning SD=0.31 percentage points:
- 40 um porosity outcomes [19.69,20.00,20.31]
- 50 um outcomes [20.09,20.40,20.71]
Both sample SDs are0.31; means differ0.40 percentage points, so the README accepts.
- Assuming independent normal observations, SE of difference =0.31*sqrt(2/3)=0.253114.
- df4, 90% interval half-width0.539600; 95% half-width0.702757.
- The 90% interval for the -0.40 difference is [-0.93960,0.13960], not contained in ±0.5. Even an observed zero difference with these SDs would have a90% interval wider than the tolerance.

This is illustrative arithmetic, not KG50 observed scatter. The prior0.31 SD does not establish scatter for any of the other three metrics or for any other SE diameter. The formula is the standard two-sample mean-difference interval ([NIST](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/diffmean.htm)). It does not imply that six runs must be increased before any pilot is allowed.

D3 as the coarsest SE gives a useful engineering screen, but a common largest AM diameter does not impose a monotone bound on finite-size error of transport networks. L/D_AM is6.67 versus8.33; AM/SE diameter ratio changes from2 at D3 to8.57 at D0.7, and path connectivity/correlation length is not fixed solely by the largest particle. A pass for D3 therefore demonstrates only D3 behavior at these two sizes/seeds. Single-seed main comparisons cannot distinguish a small size effect from realization scatter; the user's accepted single-seed scope is a reporting limitation, not a newly introduced mandatory simulation campaign.

Minimal remedy: label this an exploratory D3 engineering gate; define the relative denominator (e.g. 50-um mean) and nonfinite/nonspanning cases; classify uncertainty crossing a tolerance as inconclusive instead of equivalent. If general finite-size invariance is required for final claims, obtain evidence for the relevant other diameter(s) or state the unverified transfer. Do not quietly widen the thresholds after results.

## Direct answers and non-blocking checks

### Q3: Skin 2 ->0.5 um

No intrinsic change to the specified contact law or an unavoidable contact-history-loss defect was found in pinned source just from setting skin0.5 before running:
- neighbor.cpp:1385–1460 checks particle displacement every step with the effective supplied every1, delay0, check yes; trigger=skin/2.
- neigh_gran.cpp:579–597 uses (ri+rj)*contactDistanceFactor+skin and restores live overlap histories by particle tags.
- fix_contact_history.cpp:305–414 preserves contact histories through migration.
- normal_model_hooke_hysteresis.h:257–261 clears deltaMax for non-overlapping surfaces, so this model has no demonstrated finite separated-pair history range that would require skin2.
- Moving mesh has its own displacement trigger at skin/2: multi_node_mesh_I.h:792–825; fix_mesh.cpp:579–582 requests the next neighbor rebuild.
- fix_neighlist_mesh.cpp:249–263 uses full neighbor skin for moving mesh, half skin for stationary mesh; it does not leave the mesh list permanently at an old2-um range.
- pair_gran.cpp:623–634 sets type cutoffs from max radii; comm.cpp:456–477 builds single-style ghosts from max neighbor/fix range. Ordinary pair cutoff is6+skin, hence8 ->6.5 um.

These source facts support a convergence-testable numerical tuning choice, not an exact trajectory identity guarantee. Run-order floating-point differences and rebuild timing can change trajectories. The current fixture has no mesh and cannot test the mesh portion of this claim. The installed binaries remain unverified. The official check/timestep/gran diagnostic also checks skin divided by relative per-step displacement ([pinned documentation](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/fix_check_timestep_gran.txt#L59)).

At physical plate speed10 um/s and dt1e-6, mesh displacement is1e-5 um/step. Half-skin intervals from mesh motion alone are100,000 steps for skin2 and25,000 for skin0.5, plus the implementation's next-step trigger. Particle motion can rebuild sooner. This is a quantitative reason that a 20k fixture with no mesh says nothing directly about mesh-trigger frequency.

### Q5: Insertion feasibility

NP1 removes the demonstrated narrow-subdomain impossibility. It does not make maxattempt3000 a success guarantee. At the nominal40-um target, n*maxattempt=937,518,000 fits signed int32, and insertion_ratio=0 at this one-shot empty start. The source uses a shared per-rank trial budget, not3000 independently guaranteed successful trials for each particle. A difficult early particle can exhaust it. Low overall solid fraction0.321 and large-first insertion are favorable conditions but insufficient to prove all specified seeds fit.

The only pre-production confirmation is an actual permitted NP1 insertion test with total and phase counts and its checkpoint inspected; none was run in this review. Existing99% and AM gates are sensible failure detectors and must be retained. A passing total gate alone never proves the requested phase composition. For the already supplied NP28/56 speed jobs, feasibility is stronger than uncertain: D1 establishes the source-level geometric failure.

### Q6: Time and parallel arithmetic

50–60 um/(10 um/s)=5–6 s, with dt1e-6 gives5–6M moving steps; plus0.5M settling/stabilization/relaxation gives5.5–6.5M, consistent with an order-of-magnitude5–7M estimate. Actual movement to reach target pressure is not established by that arithmetic or by the cited pure-SE prior run. Initial plate clearance/stabilization and pressure response matter.

The stated NP56 subdomain dimensions are correct. Halo width8 um exceeds both; with skin0.5,6.5 um still exceeds both. In a uniform-density XY-only halo approximation:
- NP28 skin2: ghost/owned ratio8.88; skin0.5:6.5325.
- NP56 skin2:14.96; skin0.5:10.79.
These are geometric communication-volume indicators, not measured counts or an MPI efficiency estimate. Multi-hop halo communication is supported; narrow cells alone are a cost problem during dynamics, not automatically an invalid decomposition. They are an impossibility during guarded AM insertion, as D1 shows.

The neighbor count heuristic reproduces approximately138,65,19,11 for rSE0.35,0.5,1,1.5 at phiSE0.30, skin2. It is a full sphere-volume heuristic that ignores pair correlations and mixed contacts; it is not measured neighbor count, contact count, or per-particle CPU cost. Thus the old single-core cost and these ratios cannot establish1.5–3 days. The corrected range is a planning estimate awaiting representative timing.

## Reproduction

Run probe_design.py with ordinary Python3. It reads fixed inputs and pinned saved sources, verifies24 Git blob hashes, asserts key source predicates, exhaustively enumerates allowed XY factor pairs for NP28/56, and writes probe_design_results.json. It contains no simulation, MPI, cluster or network call. The probe passed.

No baseline physical-law validity conclusion, no completed insertion claim, no deployment binary match, no benchmark timing, and no finite-size convergence result is asserted.

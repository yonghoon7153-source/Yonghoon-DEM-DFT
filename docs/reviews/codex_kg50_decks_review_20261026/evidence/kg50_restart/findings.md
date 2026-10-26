# KG50 restart / insertion review evidence

Scope: fixed user-authorized snapshot bytes for claimed commit 3056eef12b60ed754fa59ec5a84fad811b14c9c8 (not yet pushed), Q1/Q2/Q4/Q8. Upstream reference is official CFDEMproject/LIGGGHTS-PUBLIC commit 3d5c00f20519e6bb6eb6756f51f1ad36564e649d. Actual server executable and external dem_restart.py are not available. No simulation, MPI, WSL, remote host or real scheduler operation was run.

## P1 — resume trial failure can still trigger the production submission branch

Repository: scripts/resume_ckpt.sh lines67–74,76–95,107–109.
Best tight review location: lines93–95 (empty intersection is reported as “original log has no regular row”, even when the original has1000/2000/2001 and the trial has none); also lines67–74 for missing success-status check.

The intended D0.7 route in README.md58 explicitly relies on this helper before submitting the multi-day production run. The status wait accepts FAILED/CANCELLED/TIMEOUT/OUT_OF/NODE_FAIL merely to exit its loop. It never requires COMPLETED or exit0. G1 only requires matching step1 and no uppercase ERROR token. G2 defaults to1 when settling has no step1 dump, as this insertion deck does. G3 sets1 if the intersection of regular thermo rows is empty. The final production submission tests only G1/G2/G3.

Synthetic source-guarded predicate reproduction:
- Original insertion log has valid1,1000,2000,2001 rows.
- Trial marked FAILED has only matching step1 then “MPI process exited on signal11”, no LIGGGHTS uppercase ERROR and no Loop time footer.
- G1=G2=G3=true, F2 absent; source main submission branch is selected.
- Failure after matching step1000 also selects the main branch.
- Healthy full trial passes; doubled KE at1000 and explicit ERROR fail as negative controls.

This is a proven helper logic defect by source inspection plus a Python translation with source assertions. It is not a real cluster failure reproduction. The exact extracted Bash harness was prepared but Git Bash failed before execution due sandbox named-object access. See probe_resume_gates.py, shell_execution_limit.txt, probe_source_semantics.py and semantic_probe_results.json.

Minimal fix: require the trial job's terminal state COMPLETED plus ExitCode0:0, require the expected final timestep (2001 for this2000-step run from restart1) and completed-run footer, and require at least the expected shared regular row when the source log covers the trial. Empty trial/source intersection must not be treated as absent source coverage. Gate production submission on those predicates as well as G1–G3; fail closed on timeout or unavailable scheduler/log data. Matching all planned thermo rows is preferable to first-row-only comparison, although normal different-NP floating point divergence remains expected.

## Q1 — rank-local allocation is real; compulsory systematic AM undercount is not

Official fix_insert.cpp414 sets exact_number=1;682 distributes total among ranks;695 generates each rank's particle list. fix_particledistribution_discrete.cpp147–159 converts mass to number weights. In398–450 each rank floors n_local*w_i, then assigns missing slots using the fractional remainders. With this deck's TWO templates, missing slots are0 or1, so each local AM count is floor orceil of expectation. Under uniform remainder selection the expected count is preserved. A repeated fixed-seed observed deficit does not establish a systematic bias inherent in the floor operation.

At D0.7 N=312506, AM number fraction=0.003033546734740726 and AM expectation948.0015558868853. NP1 allocation can produce948 or949. Illustrative even NP56 rank counts5580/5581 permit total AM896–952 depending on remainder outcomes; this is an algorithmic bound/counterexample, not a replay of actual PRNG seeds or successful geometry. NP1 sensibly limits composition variation and avoids rank-small insertion geometry issues, but does not mean every phase count equals the generator-rounded plan exactly. Existing SELF-70 excerpt already retracts its former universal failure assertion.

Correct documentation to “rank-dependent stochastic phase-count variation; fixed seeds may give a deficit; NP1 reduces variation,” retaining AM/total gates. Generated comments at make_se_size_decks.py299–300 and deck lines13,18,134 currently overstate systematic deficiency.

## Q1 — NP1 step1 checkpoint to different NP is supported, conditionally

read_restart.cpp206–248 explicitly redistributes stored atom records to current subdomains and569–587 only warns when processor count/grid differ. doc/read_restart.txt31–51 documents changed-NP floating point divergence and granular half-step/full-step velocity restart differences. This is supported continuation, not a promise of identical future trajectories.

The generated insert deck has total gate128–132 and AM gate135–140 BEFORE write_restart156; failed count checks cannot emit this fresh step1 checkpoint. It unfixed ins_mix124, and the checkpoint is before settling integration and mesh creation. A stated zero-contact initial state reduces contact-history restart concerns; its actual realization still needs runtime evidence. write_restart.cpp166–190 initializes and exchanges particles before writing;210–225 checks inconsistent atom count.

The resume deck must restore all required fixes/material properties, neighbor/communication settings, timestep and computes; fixes are not automatically reinstantiated (doc/read_restart.txt112–123,130–137). It must NOT reinsert. resume_ckpt.sh43–46 adds template/distribution fixes, but correctness/completeness of the other reconstruction and exact remaining settling count cannot be established without the external ~/dem_test/dem_restart.py or its emitted deck. Source-side original phase1 ends at200001 (start1 + run200000), not200000. This is a verification prerequisite, not a proven defect in unavailable code.

## Q2 — nominal thermo schedule works, but gate strength is limited

The insertion deck sets thermo_style custom step atoms ke cpu at144, thermo1000 at145, writes restart1 at156, and runs2000 at157. Official output.cpp301–313 always emits the setup row, schedules multiples of1000, and includes the last step;434–449 emits the final row. Expected stage1 rows are1,1000,2000,2001. Thus nominal matching logs can satisfy G1 at1 and G3 at1000. Original earlier run1 has a different thermo header but tl retains the last matching row.

G2's no-dump settling fallback is only redundant KE/count agreement from G1; it does not compare particle IDs/types/positions/radii or demonstrate a matching spatial state. If the review standard is “same checkpoint state,” save a step1 particle dump or checksum including id/type/x/y/z/radius/v/omega and compare that before continuing. This is validation scope, separate from the P1 failed-trial promotion.

## Q4 — quit1 is invalid syntax but does abort nonzero in the referenced3.8 source

input.cpp1110–1113: Input::quit rejects any arguments with error->all(...,“Illegal quit command”). error.cpp158–183 prints ERROR, finalizes MPI, and exits1. Consequently the true if branch prints its FATAL message then terminates before the checkpoint on this version. The requested guard purpose is met. It is not correct to describe quit1 as supported exit-code syntax. Replacing it with bare quit may lose failure exit semantics, so do not change it casually; use a version-supported explicit abort or preserve/document the intentional invalid-command abort and verify on the actual executable.

## Evidence and limits

- semantic_probe_results.json: five gate cases plus two-template number rounding.
- probe_source_semantics.py: successful source-guarded Python reproduction.
- probe_resume_gates.py: exact-source isolated Bash harness, NOT executed successfully.
- upstream_sources.json and upstream_* files: official source snapshots, URLs and blob hashes.
- Source assertions and mathematical counterexamples are not runtime insertion success, real binary compatibility, or proof that unavailable dem_restart.py is correct.

## Q1 addendum — rank RNG correlation matters

PDD constructor84 passes proc_shift=true; random.cpp69–77 offsets the seed by rank, random_park.h56 defaults multiplier1, and random_park.cpp74–79 uses the Park-Miller first draw. Thus ranks do not get independent first remainder draws. For supplied hypothetical equal local totals5580/5581, newD0.7 PDD seed11300017 produces draws0.43810568–0.43853613 and AM952; oldSELF-70 seed32452867 produces0.98812067–0.98855112 and AM896. This explains why a fixed seed can repeat a deficit while another gives a surplus; the sign is not mandated by truncation. See probe_seeded_rounding.py and seeded_rounding_results.json. This is source-guarded algorithmic reproduction with supplied rank totals, not successful insertion or actual allocator/PRNG runtime.

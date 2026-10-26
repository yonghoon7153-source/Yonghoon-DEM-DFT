# KG50 generator and deck audit

Reviewed exact attached bytes for claimed commit `3056eef12b60ed754fa59ec5a84fad811b14c9c8`; no shared Git operations or production edits. The main-deck generation transforms and independent numerical values pass. One output-fidelity issue is confirmed below. Speed-insertion and resume issues are being reviewed by sibling agents; they are not duplicated here.

## Confirmed P2: thinning atom output loses the requested end-of-relaxation state

Location: `scripts/make_se_size_decks.py:321-330`, especially the 50,000 atom-dump replacement. Concrete generated instance: `docs/data/kg50_decks_20261026/kg50_d07_b40/input_kg50_d07_b40.liggghts:208`, with `run 5000` at 216, contact cadence at 227, final `run 100000` at 233, and the final print at 234. The same pattern is present in all nine main decks. The intended observable includes the end of relaxation (`docs/50kg/dem_plan_20261026.md:35`).

The execution steps are `run 1`, settling 200,000, `run 1` for zmax, stabilization 200,000, `k` compression chunks of 5,000, and relaxation 100,000. Thus compression ends at `400002 + 5000*k`, and the final step is `500002 + 5000*k`. Atom output is on multiples of 50,000; contact output is on multiples of 10,000; mesh output is on multiples of 5,000. There is no explicit terminal dump/export.

This is not an assumption about a newer LAMMPS release. Pinned PUBLIC source at `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`, `src/output.cpp:229-239,331-346`, explicitly schedules dump output on interval multiples and does not force a dump at the last step of a run. The source is saved by the restart agent in `../kg50_restart/upstream_src_output.cpp`, with commit/blob provenance in `../kg50_restart/upstream_sources.json`.

Counterexample (integer schedule model, no simulation): for `k=1019`, compression ends at 5,495,002; relaxation ends at 5,595,002. The last atom and common atom/contact/mesh frame is 5,550,000, only 54,998 steps into the specified 100,000-step relaxation. The newest contact file is 5,590,000; pairing each stream's newest file would mix states. The newest mesh is 5,595,000. Across `k mod 10`, the saved common-state relaxation age varies from 54,998 to 99,998 steps, which can differ across SE cases.

The old atom interval 5,000 lagged the final state by two steps. Its last common atom/contact frame lagged by two steps for even k and 5,002 for odd k; the new common frame can lag 45,002 steps. The increased stale-state window is caused by this change, not a request to redesign the base physics. Whether a specific observable changes appreciably over that window remains unmeasured; the defect is that the stated terminal state is not saved for analysis.

Minimal remedy: retain the economical 50,000-step intermediate cadence but export a synchronized terminal atom/contact/mesh state at the actual end of the 100,000-step relaxation, using syntax validated against the target build. An explicit terminal restart would also preserve recovery of that state. Do not silently extend relaxation to align a grid, because that changes the registered protocol.

Bounded acceptance: a short authorized target-build check must produce the terminal files at the final thermo step, with identical step numbers and the required columns; a generator/fixture test should cover all ten compression-loop residues. Postprocessing should require matching timesteps. No target-build execution was performed in this review.

Reproducible evidence: `probe_terminal_cadence.py` and `terminal_cadence.json`. The probe parses actual deck periods and run counts, evaluates all ten residues, and executes no LIGGGHTS command.

## Passing evidence

- `selftest.txt`: permitted generator selftest is 81/81 PASS.
- `generation.txt`, `regenerated/`: the README command regenerated 38 files, including the manifest, exactly byte-for-byte with the attachment. This includes nine main decks, nine insertion decks, runners and four speed decks.
- `audit.py`, `audit-output.txt`, `independent_audit.json`: 86/86 independent checks pass. The executable-command skeleton, with only the fifteen enumerated changed slots removed/normalized, is identical to the base for all nine main decks. Full per-deck unified diffs are saved. The material, contact law, timestep, pressure, motion, damping, walls, and phase commands outside the enumerated slots remain unchanged.
- Every insertion deck prefix is byte-identical through the main deck's step-1 checkpoint line; its only further executable line is `run 2000`.
- All 45 main-case seeds are independently tested primes in the allowed eight-digit range, are unique, and lie below the ps45 band. The generator selftest checks all 60 main/fallback seeds. Speed seeds equal the intended D0.7-40 seeds.
- Both pressure areas independently parse as 0.0016 or 0.0025; density is AM 4.85/SE 1.64, AM radius is 3 µm. Independent target-loading arithmetic gives zero-porosity thickness 101.98161487375943 µm. The rounded insertion region height is 317.700 µm (z 0.005 to 0.322700 in simulation units).

| Case | AM | SE | Total | maxattempt × total |
|---|---:|---:|---:|---:|
| D0.7-40 | 948 | 311,558 | 312,506 | 937,518,000 |
| D1-40 | 948 | 106,865 | 107,813 | 323,439,000 |
| D2-40 | 948 | 13,358 | 14,306 | 42,918,000 |
| D3-40 | 948 | 3,958 | 4,906 | 14,718,000 |
| D3-50 | 1,481 | 6,184 | 7,665 | 22,995,000 |
| fallback D0.7-50 | 1,481 | 486,810 | 488,291 | 1,464,873,000 |
| fallback D1-50 | 1,481 | 166,976 | 168,457 | 505,371,000 |
| fallback D2-50 | 1,481 | 20,872 | 22,353 | 67,059,000 |

The rounded-region count prediction was recalculated without calling `predict_counts`, using parsed dimensions, phase volume fractions and sphere volumes. An independent requested-loading mass calculation agrees within integer/region rounding. Predicted loading is 6.4999866 mAh/cm² for 40 µm and 6.4988896 mAh/cm² for 50 µm.

Fallback CLI output is saved in `fallback50/`; `audit_fallback.py` and `fallback-independent.json` independently confirm its counts and overflow bound. The worst optional case has a margin product 1,904,334,900, below 2,147,483,647. Integer-boundary mutations verify the generator accepts maxattempt 3383/rejects 3384 for D0.7-50, accepts 9806/rejects 9807 for D1-50, and accepts 73901/rejects 73902 for D2-50.

`audit_speed.py` and `speed-independent.json` confirm all four speed deck tails are `run 20000`, have the expected 2/0.5 µm skin, omit the AM gate as documented, retain the total gate, and share seeds with the D0.7-40 main deck. It also independently enumerates all xy factorizations: NP28's largest possible minimum subdomain width is 5.7142857 µm and NP56's is 5.0 µm, both smaller than the 6 µm AM diameter. The source-backed insertion consequence is in the sibling design review.

## Nonblocking integer-boundary precision

`make_se_size_decks.py:297` uses floor on the lower AM bound and ceil on the upper bound. Therefore the emitted limits allow one integer outside a strict ±0.5% band:

- Plan 948: 943–953 allows ±0.527426%; strict limits would be 944–952.
- Plan 1481: 1473–1489 allows ±0.540176%; strict limits would be 1474–1488.

The boundary model confirms lo−1/hi+1 fail while lo/hi pass. `make_ps_sweep_decks.py:221` floors the 99% total threshold; D3-40 accepts 4856/4906 = 98.98084%, whereas strict >=99% would require 4857. These are one-particle slack, not demonstrated multi-day-invalidating defects. If exact percentages are intended, use ceil for the total/lower AM bound and floor for the upper AM bound and update the integer tests. Otherwise state the actual integer intervals as the contract.

## Scope limits

No solver, MPI, cluster, WSL, shell launcher, or simulation was run; source files were not edited. All generated files and audit scripts live only under this evidence directory. Static counts and overflow safety do not establish geometric insertion success, restart equivalence, or physical validity. Those are separate runtime/source questions, not claimed closed by the 81/81 selftest.

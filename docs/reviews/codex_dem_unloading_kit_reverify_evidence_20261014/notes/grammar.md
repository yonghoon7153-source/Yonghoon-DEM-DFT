# Grammar, state-machine and registration recheck

Scope: read-only review of authorized snapshot `a30fe150e21f66aea2f1c360593e1cd781689b14`. No LIGGGHTS, DEM, MPI, remote execution, production source edit, ledger edit or Git mutation. The source-level reference is the previous review's hash-pinned LIGGGHTS-PUBLIC `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` files. Native grammar success is not inferred from Python selftests or from a scalar model.

## Fixed-version output and input semantics

- `upstream/output.cpp:224–245`: provided output is enabled, fixed-period setup writes when `step % N == 0 && last_dump != step`. This is not an unconditional iff: `last_dump < 0 && first_flag == 1` is an independent first-write condition. `dump.cpp:112` defaults `first_flag` to zero.
- `output.cpp:240–245` evaluates a variable period at each run setup, whether or not a setup frame was written. `output.cpp:339–355` reevaluates after each scheduled output. The value is cast to an integer and must be strictly greater than the current timestep. It is an absolute next timestep, not a period length. `output.cpp:331` says the end of a run does not itself force a dump.
- `run.cpp:209–218` performs output setup even with `pre no`; normal runs initialize the system and `verlet.cpp:196` calls output setup. `output.cpp:175–181` resolves variable indices on initialization. The initialized variable definitions must therefore remain valid, and reassignment between runs is supported by reinitialization.
- `output.cpp:638` sets a newly created dump's `last_dump=-1`; `Output::init` does not reset it. Consecutive runs in one process therefore suppress same-step duplicates, while a recreated fixed dump can emit the aligned restart step. State files do not serialize the output object's last-dump clock. `input.cpp:671–676` destroys/recreates simulation state on `clear`.
- `input.cpp:221–231` returns from an include at EOF to the parent input. `input.cpp:845–846` prohibits an include within an if command. `input.cpp:867–909` allows the subsequent parent `jump SELF label` when the outer input was supplied through `-in`, rewinds that parent, and scans for the label. This source review does not execute a real include or restart.
- Repeated linear `move/mesh` is incremental (`mesh_mover_linear.cpp:94–111`). Unfix unregisters movement and resets retained mesh velocity (`fix_move_mesh.cpp:141–162`), consistent with repeated movements. This does not substitute for the requested native fixture.

## Correction to the previous review's offline probe

The old `probes/deck_control.py` processed each dump in turn and changed its shared `self.step` while enumerating one dump's frames. It failed to restore the common setup time before evaluating the first frame of the next dump ID. Consequently, later variable-period dump IDs could omit early frames in the *model*. This is a Codex probe defect, not a finding against the producer.

The new `probes/grammar_recheck.py` keeps one common setup time and processes all due dump IDs chronologically. It covers identical schedules for three IDs, variable setup suppression, reevaluation at setup and after output, fixed aligned setup de-duplication, recreated dumps, the `first yes` exception, and nonfuture-step rejection. These are reference-model checks cross-read against the C++ source; the model cannot validate its own native grammar assumptions.

Re-running the old pinned production decks with the corrected scheduler preserved the prior substantive results: early recontact still moved k=5 to k=6 at w=4 with 8 windows remaining, late declaration still ended DONE at w=15 under a nominal 12-window budget, and G_UVa/G_UVb still had initial 4–12 and later 8–24 budgets. The old normal trace now has synchronized atom/wall/pair schedules. The previously reported absence of non-mesh movement/setup frames remains true. Thus ULKR-07/10A did not depend on the probe clock bug.

Evidence: `evidence/grammar_previous_scheduler_corrected.json`. The old late-declaration outcome will be judged against the new explicit registration, not automatically called a residual defect if the registration now separates the declaration budget from four post-declaration windows.

## Selected snapshot review

### New finding: the required grammar fixture reads a scalar ave/time fix as a vector

Exact producer locations:

- `source/docs/data/ps45_unload_20261009/history_test/make_history_decks.py:732`: `fix gr_av all ave/time ... v_Ps` has one scalar input.
- Same generator `:765`: `variable gr_P equal f_gr_av[1]`, followed by immediate `${gr_P}` freezing.
- Generated `history_test/in.hist_grammar.liggghts:77` defines that fix; `:132–133` reads/freezes the indexed expression after the first `run ${gr_W}`.

The fixed upstream defaults `fix ave/time` to SCALAR mode (`fix_ave_time.cpp:861`). One scalar input exposes a global scalar (`:350–364`); multiple scalar inputs expose a global vector (`:366–368`). `variable.cpp:1182` accepts `f_ID` for a scalar, while `:1198` requires a vector for `f_ID[i]`; otherwise `:1315` raises `Mismatched fix in variable formula`.

Therefore the present GA is source-provably unable to finish its first window's observation: after the 2000→2100 run, freezing `${gr_P}` requests a vector element from a scalar. It fails before the first `GRAM_STEP`, restart/state write, repeated movement or GB resume path. This is a source proof of the native error, **not an observed native error log**; no simulator was executed. The expected successful H0–H5/SYN files remain separate and unaffected.

The synthetic model hides the mismatch: `grammar_sim` at `make_history_decks.py:813` replaces every `f_*`, including bracketed forms, by `0.0`. Our in-memory variants using the actual `f_gr_av[1]`, corrected `f_gr_av`, and impossible `f_gr_av[999]` all yield identical successful model traces. A passing generator model is consequently incapable of validating this part of grammar.

Minimum repair: correct the generator to scalar `f_gr_av` (or intentionally define a multi-value ave/time output), regenerate the grammar deck and seal, and add a negative type-access fixture that rejects the current scalar-with-index form. Then run the authorized real fixture and inspect its actual report before claiming native coverage. The producer files were not edited during this review.

Evidence: `evidence/grammar_deck_recheck.json`, `grammar_fixture.native_blocker` and `producer_model_blind_spot`. This requires a new finding ID; it is not a residual instance of ULKR-07 or ULKR-10.

### ULKR-07 generator/control-flow portion: close against registration revision 3

The new `_machine` adds `ul_rc`, routes recontact to `ul_win_rc`, and stops at exhausted budget (`make_unload_decks.py:362,373–380`). Independent execution of the actual committed scalar branches gives:

| Synthetic contact case | New outcome | Contract |
|---|---|---|
| First separation w2; recontact w4 | k remains 5, re-declaration w6, DONE w9; no movement | Same height, remaining budget |
| Recontacts w4/w8; contacts w9/w10; re-declaration w12 | k remains 5, DONE w15 | Valid: declaration within 12, four post windows include w12 |
| Contact again at w12 | SEP_INCOMPLETE at k5/w12; no movement | Exhausted same-height budget |
| Re-declaration w12; contact w13 | SEP_INCOMPLETE at k5/w13; no movement | Post observation can exceed budget, but renewed separation cannot |

The normal path remains DONE; atom/wall/pair dump schedules agree, and non-mesh setup/movement dumps remain absent. These observations are synthetic and concern control only. The reader-side closure belongs to the lead review's independent reader checks.

The old w15 result is intentionally no longer a negative fixture by itself. REG `dem_unloading_ps45_prereg_20261009.md:891–895` now explicitly allows four post-declaration windows, starting with the declaration window, outside the declaration budget. It is a pre-result, author-approved interpretation of the previously open budget relationship. Do not report this as an unchanged bug. The fix-plan table's loose phrase “four more” should be read through this precise rule; declaration at w12 ends at w15, not w16.

### ULKR-10A: close, with the registered interpretation explicit

REG `:882–883` confines gravity's 4–12 exception to its first k=0 equilibration; later B/confirmation/separation holds inherit the parent tuple. All 20 G decks independently yield initial 4–12, later 4–12 for UB/UT3 and 8–24 for UVa/UVb, with stable later exits at 4 and 8 respectively. Generator lines `:440–445` change only k0 limits; README `:200–201` now says the same. This satisfies the prior report's requested result-before-data scope decision and per-deck table. S3 g wiring (10B) is outside this subreview.

### Q4: coverage design present; native closure open, with a concrete blocker

README `:132–147` and the actual grammar deck cover the four originally missing construction paths: outer include followed by parent SELF jump, variable-period atom/local dumps, repeated move/unfix with cumulative mesh height, and a fresh GB process using GA's final restart plus state file. The expected timestep and mesh-height table agrees with the fixed output scheduler semantics above. The missing pair dump does not omit a new variable-period scheduling *language* class: wall and pair both use `dump local`; it also does not prove the production pair observer's physical contents.

The expectation for GB's first mesh frame at 4300 is correct: the new process recreates the fixed-period dump with `last_dump=-1`, so its aligned setup emits once. In GA, the next run's setup at a timestep already written does not emit a duplicate. Variable-period atom/wall schedules are reevaluated at setup and after each output, with `first yes` absent.

However, the scalar/vector defect prevents those paths from actually being completed. Q4 cannot be marked PASS or closed on the current fixture or its synthetic model. After correcting that defect, the real binary fixture remains required; no synthetic result substitutes for it.

### Reader negative fixtures and a narrower runner/documentation mismatch

Independent single changes to synthetically generated files were fed to the actual `grammar_info` function. The normal control was PASS/rc0. Each of GA rc1 with all artifacts retained, P rc1 with all artifacts retained, missing wall-end frame, wrong header timestep, wrong restored mesh height, wrong state k, and one extra correctly headed atom frame during movement was FAIL/rc2. Thus no false grammar PASS was found in these targeted cases. This is file-to-reader validation, not evidence that native GA or GB has executed.

README `:136` says GA failure prevents GB. The runner at `history_test/run_history.sh:134–137` does not test GA's return code; it starts GB if any final-looking state/restart artifacts remain. Likewise `:130–132` tests the producer artifact after its rc failure. A failure after writing artifacts can therefore continue the small diagnostic job despite that documentation. The final reader still rejects failed stage rc (`read_history.py:708–709,785–788`), confirmed by the targeted cases, so this is not evidence of a false PASS or production release. Narrow cleanup: guard GA/GB launch on the preceding stage rc as well as files, and test failure *after* artifacts, not only failure before any artifacts exist. This is lower severity than the native scalar-access blocker.

### Q5: distinguish mandatory evidence from automatic enforcement

REG `:909–911` and README `:221` explicitly say native grammar PASS is required before production R but currently enforced procedurally. The prior review required that evidence before R; it did not mandate a particular code gate. A documented, checked native PASS attached to the source/build/fixture before GO can satisfy that procedural requirement. It cannot be inferred from the selftests or silently omitted.

A machine-enforced gate is recommended if the workflow is expected to enforce all required prerequisites automatically: check the grammar verdict and provenance before any production R/EXT launch, and also require it when issuing/reusing RESTORED. Merely adding a grammar JSON condition after R in `restore_verdict` would prevent follow-up U but would not enforce **before R**. Whether to add that policy gate remains the first author's stated decision. Its present procedural status is accurately disclosed and is not by itself a new contradiction in REG14.

### Reproduction

From the workspace, using the bundled Python (UTF-8 mode is necessary on Windows because the producer's synthetic helper writes Korean comments through default text encoding):

```text
python -X utf8 -I -B dem_unloading_kit_reverify_20261014/probes/grammar_recheck.py --kit dem_unloading_kit_reverify_20261014/source/docs/data/ps45_unload_20261009 --out dem_unloading_kit_reverify_20261014/evidence/grammar_deck_recheck.json
```

No source or ledger files are written. The temporary synthetic file bundles are deleted by their owning temporary-directory context; the full trace and outcomes remain in the JSON evidence.

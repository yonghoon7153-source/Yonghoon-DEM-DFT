# Deck review — Q2 / Q3

Pin: `2783061ead9f192ab742a2f0b14b0182a98a4966`; upstream source supplied at `3d5c00f`. Read-only review of `source/`; no DEM, MPI, SLURM, production restart, or native simulator execution. The supplied source directory is an exported snapshot, not a Git checkout (`git status`, HEAD, and worktree commands correctly reported that fact).

Evidence: `probes/deck_control.py` interprets scalar commands and branches from the actual committed `decks/ps_7_3_r45/in.U_UB.liggghts` and gravity variants, with explicitly synthetic observation inputs. It stubs all particle/model operations. `evidence/deck_control.json` is the complete trace. This is an independent offline control-flow probe, not the kit's string-presence selftest and not native LIGGGHTS syntax certification.

Reproduce from review root:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -I -B probes/deck_control.py
```

## Finding D1 — P2: Recontact leaves the same-height hold early, and POST bypasses its budget

Locations:

- `source/docs/data/ps45_unload_20261009/make_unload_decks.py:368`–377, especially 375–377.
- Actual `decks/ps_7_3_r45/in.U_UB.liggghts:228`–252; ordinary steady exit is 231–232; recontact jumps to it at 252.
- Contract `source/docs/reviews/dem_unloading_ps45_prereg_20261009.md:739`–740; request Q2(e), `codex_dem_unloading_kit_request_20261013.md`.

First counterexample: begin a legal phase-2 separation hold at k=5. Every synthetic window has total KE=2e-8 below S2, guard-safe atoms and leakage. Geometric contact sequence is `[0, 0, 0, 1, 0, 0, 0, 0, ...]`; pressure is zero for zero-contact windows and a small positive 1e-8 deck MPa at recontact. This keeps S1 passing while contact state changes, without assuming zero pressure proves separation.

Expected under the explicit request to continue in the same hold budget: declare at w=2, reset on w=4 recontact, continue at k=5 using the eight remaining windows, allowing re-separation at w=6 and four post windows by w=9. Actual: declare at w=2; at w=4 set phase=2 and postw=0, then jump to generic steady logic. Since okn=3 and w>=4, the hold immediately ends, writes a step restart, and moves the plate to k=6. The next movement destroys the requested same-height observation opportunity. Clearing the separation/post counts is correct; the continuation target is not.

Second counterexample: use KE=2e-5 (S2 fails but the KE guard threshold is 0.0017), with contacts at w=4,8,9,10 and zero contacts otherwise; pressure is 1e-8 at contact and zero otherwise. Declarations occur at w=2,6,12 and recontacts at w=4,8. At the last declaration w=12, POST skips `ul_win_gen`, then consumes w=13,14,15 and reports DONE at w=15 with `ul_wmax=12`. Thus the same-budget requirement is not enforced during renewed post-separation observation. The new trace is not a DEM result; it is an exact consequence of deck branches for a legal observation sequence.

Impact: the plate position used for the surface observation can change after recontact before the remaining hold budget is used, or completion can consume a longer hold than registered. This concerns the auxiliary trajectory/surface measurement; it does not by itself invalidate a previously completed primary 1-MPa crossing. Fix should give recontact its own continuation/budget handling and document whether the four post windows are included in that budget. Regression evidence should cover recontact after w>=minimum while S1/S2 remain steady, and a late re-declaration near the maximum. The current R6 reader fixture `[0,0,1,1]` and generator keyword checks do not execute this path.

## Finding D2 — P2, registration ambiguity to resolve before results: UV gravity holds use 8–24 after the first hold

Locations:

- `make_unload_decks.py:103`–107 inherits arm `hold_factor` for `wmin` and `wmax`.
- `make_unload_decks.py:437`–440 overrides only gravity `ul_k0min` / `ul_k0max`.
- `make_unload_decks.py:363`–364 uses generic `ul_wmin0` / `ul_wmax0` after phase 4.
- Actual `decks/ps_7_3_r45/in.G_UVa.liggghts:71`–74 and 100–101 (same for G_UVb in all five beds).
- Prereg C10 at line 798 explicitly excludes gravity holds (4–12) from UV ×2; C12 at 806 says gravity hold 4–12; kit README line 150 also says gravity hold 4–12.

Evidence `gravity_budgets`: G_UB and G_UT3 have first/later hold budgets 4–12; G_UVa and G_UVb have first hold 4–12 and later hold 8–24. Constant, fully steady synthetic pressure after the first B movement ends those holds at 8 windows, not 4. This is encoded in all ten G_UV decks.

If C10's exception was intended only for the initial gravity-change equilibration, this is a documentation ambiguity rather than an implementation error. Current published wording does not contain that restriction; either make all gravity holds 4–12 or explicitly register the narrower exception before any results. Do not silently treat the 8–24 implementation as already authorized by C10.

## Q2 checks with positive evidence

- Last two windows: `_window_read` freezes pressure before updating Pprev, records `(P+Pprev)/2`, and hold end adopts this quantity (generator 305,314,379). Synthetic P=[0.00242,0.00244,0.00246] ends k=0 at Pbar=0.00245, exactly the last-two mean.
- B switch: only SEARCH executes the Pbar<=3Pm branch; k=0 routes through its own handler. Probe confirms low k=0 pressure does not turn on B. In ordinary fixture k=1 reaches 2.5 MPa and the next move is B.
- First-cross confirmation: crossing sets modeB=1, and two later step completions trigger RM. Ordinary trace has CROSS at k=2, RM at k=4, both confirmation moves B. A lower starting pressure is separately disqualified by the reader's crossing rule; deck CROSS alone is not proof of a valid bracket.
- Separation declaration counting: ordinary trace declares on second zero window w=2; declaration initializes postw=1 and DONE occurs at w=5, giving exactly four post windows including the declaration window.
- Cap C11: B motion from lift .01595 to .016 is allowed; from lift .016 toward .01605 is suppressed and reports LIFT_CAP. Actual comparison is prospective lift > cap+dzB/2, matching the ratified discrete rule.
- k=0 UNSTEADY routes to TECH and does not move; later UNSTEADY holds continue with labels, as prereg line 337 permits.
- Control-flow limitations D1/D2 remain; these positive cases do not close all of Q2.

## Q3 source semantics: no confirmed syntax blocker in the requested constructions

1. `include ${ul_state}` followed by `if ... "jump SELF ul_resumed"`: include pushes the input file; input EOF pops back to its parent (`upstream/input.cpp:221`–233). Thus the following SELF jump rewinds the outer deck, not the finished state include. `include` inside if is rejected at 845–846, but this deck puts it outside. `jump SELF` requires an actual `-in` file, and the runner provides one (`run_unload.sh:137`–139). Jump label scanning skips variable substitution until the target label (`input.cpp:369`, 867–909), so scanning past definitions does not execute them.

2. Variable lifetime: equal variables may be redefined (`variable.cpp:377`–393), and `${name}` is expanded before a replacement definition executes. `_freeze` therefore replaces run-dependent expressions by values, avoiding stale compute reads after write_restart. String variables also allow same-style replacement (303–320). Replacement shifts variable indices (`variable.cpp:744`–766), but normal `run` initializes the system each time (`run.cpp:209`–212); `FixAveTime::init` re-resolves names (494–515), as does `Output::init` for dump variables (`output.cpp:175`–181). No commands mutate these variables during a run.

3. Variable-period dumps: `output.cpp:229`–245 writes at setup only for fixed periods or explicit `first yes`, then computes the future step for variable periods; `output.cpp:339`–355 reevaluates after each write. With `floor(step/W)+1` the next step is always a future W boundary; movement resets the formula to `step+1e9`; every following ordinary run redoes output setup. The independent output-schedule model sees no non-mesh setup dumps and no non-mesh movement dumps in the ordinary full path. Gravity deliberately uses `first yes` for run-0 restoration. Mesh dumps remain fixed-W during movement, as the explicit C17 exception says. This is source-level evidence, not a substitute for the pending real syntax run.

4. Repeated `fix ul_mv ... move/mesh` / unfix: linear movement is incremental, `dx=v*dt`, with no accumulated reference-position jump (`mesh_mover_linear.cpp:94`–111). Creation/deletion registers/unregisters movement (79–86); `FixMoveMesh::pre_delete` explicitly zeros retained mesh velocity (143–148) and unregisters its caller (159–162). No source basis found for a repeated-definition prohibition or second-move displacement reset.

5. `region NAME delete`: recognized region deletion removes the matching region, allowing recreation (`domain.cpp:1351`–1353 and 1407–1416). Geometric counts resolve region identifiers rather than retaining deleted pointers (`variable.cpp:2907`, 3100). Existing SYN already exercised deletion/redefinition.

6. Persistent `fix ave/time` across separate runs: it is defined once; `init` preserves its next sample unless genuinely overdue (`fix_ave_time.cpp:518`–523). nvalid advances after every sample and completed averaging block (608–619); `compute_vector` returns the last completed average (831–835). W, movements, starting steps, sampling and output periods align, so the final hold read is a full hold window. Reading fix averages between runs is allowed by `variable.cpp:1203` (compatibility test applies only in a run). Existing SYN provided real-binary evidence for this construction.

7. `compute wall/gran/local id force_normal`: keyword flags determine fixed column order, not argument order. ID columns are mesh index, triangle ID, atom ID (`compute_pair_gran_local.cpp:679`–683 and 777–780), followed by projected normal force components (789–799). This gives six columns in the order used by the deck/reader. For R `id history force_normal`, the fixed ordering is ID, normal force, then history, irrespective of keyword order; inherited history evidence is consistent with that.

Residual verification: native SYN did not run include/resume, variable-period dump schedules, or multiple move/unfix cycles. Add these to an authorized small-fixture syntax regression before claiming native Q3 closure. No production execution is justified solely by this offline probe.

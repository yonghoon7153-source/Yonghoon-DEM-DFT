# R10 snapshot / provenance / producer-boundary adversarial review

Target: `bd6ba4749a92f8d441b4d9176eb876bfc6cc287c`  
Scope: `bms-balancing/` only; target worktree was not edited.  
Executable reproducer: `outputs/r10_snapshot_repros.py`  
Captured result: `outputs/r10_snapshot_results.json`

Run:

```bash
cd <review-workspace>
PYTHONPATH=work/harness-r2-pydeps /home/yonghoon71/ddvenv/bin/python \
  outputs/r10_snapshot_repros.py \
  --target work/harness-r10-target-wsl/bms-balancing --case all
```

All seven cases reached their asserted bad result.

## Findings, in priority order

### S1 — P1 / porting identity: `eval --out X --compare X` destroys the independent evidence and certifies Python against itself

- Code: `bms_balancing/verify.py:1083-1091` writes `args.out`; only afterward `:1093-1098` calls the comparator, whose first read is at `:1142`.
- Repro: `--case eval-self-overwrite` begins with an intentionally invalid independent file. `cmd_eval` overwrites it, then reports 16/16 anchors and 32/32 RMSE equal, `rc=0 (complete)`.
- Observed original SHA: `c3dabc9d75d4d5e3173d808de370da45106fb7df899e601ee29913b65f973f50`; after SHA: `3d18405e59f7932df4bb69b1f4c48f40e13ed7f75adcabc991a70fb0a7ac33ce`.
- Why the R9 one-read fix does not close this edge: it reads exactly once, but it takes the snapshot **after** the producer has replaced the evidence.
- Minimum structural close: if `--compare` is present, load `DdEvalText` before any output-side effect and pass that typed snapshot into `_compare_dd_eval`; `_compare_dd_eval` must not reopen a pathname. A pathname equality check is insufficient because symlink/hardlink/bind aliases remain.

### S2 — P1 / canonical completeness: a partial profile is published as complete and accepted by the wrapper

- Code: failed gamma points are omitted at `verify.py:1572-1576`; the exact missing list lives only in stdout summary (`:1603-1632`). If at least one row survives, `:1637-1642` publishes canonical and returns 0.
- Repro: `--case profile-partial` requests two gamma points; one succeeds and one fails. It returns 0, replaces the prior complete canonical with a one-row CSV, and `schema.check_rows()` returns no problems.
- Production consequence (also executed by the repro): the real `run_states.sh` `write_meta` function signs the one-row bytes and the real `provenance.py --verify-unit` returns `일치`. Every surviving row has the current `run_id`. The sidecar roster records only `[min,max,count]`, not the requested grid or missing points.
- Minimum structural close: compute a requested gamma roster before fitting, publish canonical only for an exact complete roster, and give partial results a typed status plus a separate `partial/` destination. Put requested/succeeded/missing gamma identities in the artifact/sidecar, not only the disposable log.

### S3 — P1 / U18 provenance gate: a truthy extra `error` column disables all row validation and still earns rc 0

- Code: `schema.py:120-121` unconditionally skips every content/provenance/numeric check for a matrix row with truthy `error`. Extra columns are not rejected. `check_u14.py:239` reports an extra field only as informational `added`, and `:447` does not include `added` in `contract_broken`.
- Repro: `--case error-skip` keeps all scientific numbers exactly equal to a signed baseline, blanks `inputs_sha`, `ref_inputs_sha`, `consumed_inputs`, and `ref_consumed_inputs`, adds `error=skip all validation`, and re-signs the unit. `check_u14` prints both “새 스키마: 전부 갖췄다” and “숫자 … 전부 같다”, then exits 0.
- This directly reopens R9-03: the checker can promote a provenance-empty candidate by attaching one untyped column.
- Minimum structural close: use a discriminated union. A success row must have the exact success schema and no `error`; an error row must have an exact error schema and makes the enclosing artifact `partial/failed`, never promotable. Reject unknown columns at the promotion boundary.

### S4 — P1 / preservation and producer status: all-error matrix overwrites canonical and exits 0

- Code: each model failure becomes a four-field row at `verify.py:1404-1407`. `:1512-1515` writes whatever rows exist without a schema/completeness decision; falling off the function returns `None`, hence process rc 0.
- Repro: `--case matrix-errors` forces every combination to fail. Sixteen error rows replace the previous canonical; header is only `error,half_cell,si,w_dqdv`; `schema.check_rows` reports 36 problems; effective process rc is still 0.
- Wrapper caveat: the normal wrapper later rejects these rows because `run_id` is absent, but that happens **after** the previous complete canonical was destroyed. Direct CLI users also receive success.
- Minimum structural close: determine expected combination roster and typed status before publication. Only exact complete success rows go to canonical; partial/failed diagnostics go elsewhere and return nonzero. Never replace a complete canonical before the acceptance decision.

### S5 — P2 / stdout contract: invalid degeneracy JSON is emitted with process success

- Code: `verify.py:560-568` asserts schema only for `--out`; stdout mode prints a warning to stderr, emits the invalid JSON, and falls off with rc 0.
- Repro: `--case stdout-invalid` emits a parseable JSON object missing both receipts and `inputs_sha`; the real schema reports four problems, while effective process rc is 0.
- Answer to R10 Q2: “stdout is diagnostic” is not a sufficient machine boundary. A pipe/redirection sees a successful producer, and stderr can be discarded independently. The artifact need not be canonical for the exit status to be false.
- Minimum close: schema-invalid output always returns nonzero (preferably do not emit a bare artifact; use a typed diagnostic envelope). Tests that need incomplete objects should call a lower-level function.

### S6 — P2 / provenance identity: aggregate input digest is role-blind

- Code: `schema.py:44-52` sorts only leaf SHA values. Role and path are absent from the preimage; `validate_receipt` has no expected role schema.
- Repro: `--case receipt-roles` swaps the distinct `half_cell` and `full_cell` leaves. Both receipts validate and both aggregate to `76be1dcab00e`.
- Minimum close: version the receipt schema and hash canonical tuples `(role, normalized-path-or-object-id, sha256)`; enforce exact role trees per artifact/command. This should be the manifest digest injected by the common snapshot contract.

### S7 — P2 / sidecar replay: recorded “exact argv” is not an argv vector

- Code: `scripts/run_states.sh:173` stores `LAST_ARGV="$*"`.
- Repro: `--case argv` executes distinct vectors whose observed first argument is respectively `A B` and `A`; both sidecars would record the identical string `python3 -c import sys;print(sys.argv[1]) A B C`.
- Minimum close: serialize `"$@"` as a JSON array at the call boundary; do not round-trip through a shell scalar. Record relevant environment inputs in a typed map as well.

## Export-contract answer

The proposed build-boundary design is the correct location, but the injected snapshot must cover **every invariant role shared by ref/target**, not just the full-cell workbook: full-cell workbook bytes and the selected literature `gr`/`si` bytes must be captured once, role-keyed, and supplied to both builds. Per-state half-cell inputs can be separate entries in the same immutable manifest. Production build must have no pathname fallback once a snapshot handle is supplied. Sensitivity mode should carry two complete manifest digests (A/B), not merely two untyped file digests.

The open export contract disclosed in R10 remains an independent GO prerequisite; S1-S7 above do not count the already-disclosed target/ref mismatch as a new finding.

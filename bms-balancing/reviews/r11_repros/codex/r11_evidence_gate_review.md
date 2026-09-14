# R11 adversarial subreview — evidence gate / replay identity

Target: `bms-balancing/` at `2add074cf0c3ebfaa02b22d2311dd4330f0879b0`; declared code commit
`665c87e195007fb72f55f58f4c71ada81275c0c6`.

Scope: `reviews/evidence_gate.py`, the R7/R9/R10 replay runners, package-digest and delegated-process
handling, expected/code/evidence commit identity, and the U18 provenance fields that decide promotion.
The reviewed target was not modified. All executable mutations ran in `/tmp` clones or standalone
fixtures. Final target status was clean at `2add074c`.

## Verdict

**NO-GO.** Four P1 structural failures and two P2 identity/flag failures are executable despite the
named R10 regressions. The strongest counterexample executes bytes absent from the expected commit
while emitting `instrument_sealed:true`, `package_digest_ok:true`, `evidence_eligible:true`,
`closed:true` and rc 0.

## F1 — P1 — “materialized + instrument sealed” does not seal executed bytes

### Pre-import ignored gate bytecode

The runners import `evidence_gate` at module load:

- R7 `reviews/r7_repros/replay_codex_r7.py:25-26`
- R9 `reviews/r9_repros/replay_codex_r9.py:22-23`
- R10 `reviews/r10_repros/replay_codex_r10.py:21-22`

Bytecode isolation is only called later in `main()` (R7 `:159`, R9 `:330`, R10 `:135`). Instrument
sealing then hashes the source pathname, not the code object/module already loaded
(`reviews/evidence_gate.py:133-150`).

`early-gate-pyc` writes a timestamp-valid
`reviews/__pycache__/evidence_gate.cpython-312.pyc` whose header matches the committed source mtime and
size and whose code writes a marker. The source is unchanged and porcelain is empty. Observed:

```text
marker_executed=true, runner_rc=0, dirty=false,
instrument_sealed=true, package_digest_ok=true,
evidence_eligible=true, closed=true
```

This is the exact timing variant omitted by `test_d10_13`: that test plants invalid bytes under
`bms_balancing/__pycache__`, after the gate itself has already been imported.

### Checkout filter changes the supposedly materialized commit

`materialize()` runs ordinary Git checkout (`reviews/evidence_gate.py:83-117`) and only checks the
resulting worktree's HEAD (`:107-110`). It neither disables repository-local filters/hooks nor hashes
the materialized filesystem bytes back to the commit tree.

`materialize-smudge` commits an attribute for `bms_balancing/verify.py` and configures a repository-local
smudge driver outside the commit. The source worktree is clean. Checkout appends a marker to the
snapshot's production module; the altered module executes. Observed again: runner rc 0 and all of
`instrument_sealed`, `package_digest_ok`, `evidence_eligible`, and `closed` are true.

Package digest is functioning for the listed package files; it cannot repair either boundary because
the first attack happens before the digest code runs and the second mutates production code outside the
review package.

Minimum structural closure:

1. Bootstrap the runner in an isolated interpreter and load the gate from explicitly read, Git-bound
   source bytes; isolation after import is too late. Reject `PYTHONPATH`/startup-module injection and
   disable pytest plugin autoload for delegated tests.
2. Materialize without checkout transformations, or verify every executable/tracked filesystem object
   byte-for-byte and mode-for-mode against the expected tree after checkout. Disable hooks, reject
   external symlinks, and fail if the snapshot is dirty before execution.
3. Bind actual module origins/code digests and interpreter/dependency identity into the receipt; hashing
   a source pathname is not proof that its code object executed.

## F2 — P1 — R10 certifies nonzero delegated children as seven closed cases

At `reviews/r10_repros/replay_codex_r10.py:193-206`, each evidence child is parsed and its named boolean
is tested, but `proc.returncode` is never read or recorded. In a standalone committed fixture, the
checksum-listed child emitted the required `false` field and deliberately exited 7 for every case; its
manifest digest was updated so this is not a checksum-mismatch bypass.

Observed from `r10-child-rc`:

```text
direct_child_rc=7
parent_rc=0
instrument_sealed=true
package_digest_ok=true
evidence_eligible=true
closed=true
all seven evidence records = "반례 소멸"
```

The complete parent therefore reports its 22-case closure even though every delegated evidence process
failed. This is distinct from the fixed R9 `delegated()` path, which now binds pytest rc.

Minimum closure: require `proc.returncode == 0` before parsing/accepting the payload; validate an exact
typed child schema, include rc/stdout/stderr fingerprint in the parent record, and make any nonzero,
timeout, signal, missing case, or extra case unresolved.

## F3 — P1 — U18 promotion accepts provenance that explicitly says the candidate is unsafe

`scripts/check_u14.py:39-40,207-210` requires only the presence of
`git_commit_at_start` and `git_state_changed_during_run`. Its actual pairwise checks are limited to
`META_CONTROLS` and environment (`:223-229`); promotion is computed solely from those accumulated lists
(`:479-490`). It does not require or interpret `git_dirty`, `git_modified_code`, the value of
`git_state_changed_during_run`, or the candidate commit.

`u18-dirty-meta` used identical signed data, controls, and environment, then set candidate metadata to:

```json
{
  "git_dirty": true,
  "git_modified_code": ["bms_balancing/verify.py"],
  "git_commit_at_start": "ffffffffffffffffffffffffffffffffffffffff",
  "git_state_changed_during_run": true
}
```

The baseline commit field was forty zeroes. `check_u14` returned rc 0 and
`PROMOTION {"promotion_eligible":true,...}` with every `blocked_by` count zero.

The producer-side definition compounds this boundary. `scripts/provenance.py:68` runs status with
`--untracked-files=no`. In `untracked-sitecustomize`, an untracked repository-root `sitecustomize.py`
executed through `PYTHONPATH` and wrote a marker. Normal status showed `?? bms-balancing/sitecustomize.py`,
while provenance reported the exact HEAD, `git_dirty:false`, and `git_modified_code:[]`.

Minimum closure:

- Candidate promotion must require typed `git_dirty is false`, empty `git_modified_code`,
  `git_state_changed_during_run is false`, and a canonical full `git_commit_at_start` equal to an
  explicit expected code commit (or a documented, verified commit relation).
- Do not hide all untracked paths. Classify known output roots separately and treat untracked executable
  or importable paths elsewhere as code dirtiness. Run in an isolated import environment and record
  module origins/digests.

## F4 — P1 — R10 aliases any package-frame AssertionError to counterexample closure

`reviews/r10_repros/replay_codex_r10.py:60-76` treats any `AssertionError` whose traceback contains any
frame under the package directory as `도달:true`, `상태:"반례 소멸"`. Unlike R7/R9, it has no per-case
counterexample line/fingerprint.

`r10-assertion-alias` makes `schema.inputs_digest` raise
`AssertionError("UNRELATED production invariant")` before the receipt-role case builds its result.
The classifier returned rc 0 and:

```text
도달=true, 상태=반례 소멸
멈춘_곳=r10_snapshot_repros.py:57: return d, S.inputs_digest(d)
세부=UNRELATED production invariant
```

The neighboring exemption has the same shape: `:215-219` converts every error for the named
`shape_duplicates` case to an accepted “premise changed” state without checking its exception identity.

Minimum closure: replace inverted counterexample `assert` classification with explicit positive
predicates (`gate.need`) over typed observations. If legacy assertions must remain, bind each case to an
exact expected file/line/source fingerprint and classify every other assertion/exception as error.

## F5 — P2 — `skip-worktree` is not detected

`reviews/evidence_gate.py:153-156` says it rejects assume-unchanged and skip-worktree, but returns only
lowercase `git ls-files -v` entries. Git prints uppercase `S` for skip-worktree.

In `skip-worktree`, `ls-files -v` printed `S reviews/evidence_gate.py`,
`gate.index_skip_flags()` returned `[]`, and the actual R7 replay returned rc 0 with
`evidence_eligible:true` and `closed:true`.

Minimum closure: reject both lowercase assume-unchanged tags and uppercase/lowercase `S` skip-worktree
tags, with a regression that asserts the real `git update-index --skip-worktree` path is rejected.

## F6 — P2 — “exact expected commit” accepts a seven-character alias

All three runners use `len(exp) < 7 or not head.startswith(exp)` (R7 `:147-152`, R9 `:318-323`, R10
`:125-129`). `abbreviated-head` supplied only `2add074`; R7 returned rc 0 and recorded that short string
while setting `evidence_eligible:true` and `closed:true`.

Minimum closure: resolve the requested object as a commit, record its full canonical object id and tree
id, and compare canonical ids exactly. If the contract truly requires an exact id, reject abbreviated
input rather than merely resolving it.

## Positive controls / findings not reopened

- `python -O` is now rejected explicitly.
- Git command rc failures are fail-closed.
- A pre-run byte corruption of a listed package member is rejected, and the three current package
  manifests list every regular package file except the manifest itself.
- `--allow-dirty` structurally yields `evidence_eligible:false`.
- The current `665c87e..2add074c` diff contains only the documented ledger/request/state and replay-output
  files; the claimed `*.py`/`*.sh` diff is empty.

The code/evidence two-commit workflow is viable only as a two-phase attestation: the run can bind the
code commit/tree and instrument/package bytes, while a consumer must later bind the Git blob containing
the evidence, its ancestry, and an exact allowlist of post-code-commit changes. The runner cannot attest
the future evidence commit by itself. This is a structural clarification to R11 question 4, not an
additional counted defect.

## Already-declared open constraints (not counted again)

- Shared-input export contract remains unimplemented.
- Receipt digest intentionally omits paths pending the stated policy decision.
- Subset manifest remains unsigned; typed `(root,state,si)` identity remains a string.
- U16/U17/U18 are still user-machine measurements; current `out/` is explicitly
  provenance-incomplete.
- Partial-namespace lifetime/cleanup is explicitly unresolved.

## Artifacts

- `outputs/r11_evidence_gate_repros.py`
- `outputs/r11_evidence_gate_results.json`

Run against a clean disposable checkout with the target dependencies installed:

```bash
python outputs/r11_evidence_gate_repros.py \
  --target /path/to/disposable/bms-balancing \
  --python /path/to/venv/bin/python --case all
```

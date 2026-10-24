# Independent T12 preparation review — final v3 freeze

Verdict: PASS for the scoped synthetic consumer preparation. No outstanding implementation blocker found in the seven frozen deliverables. This is not physical T12 qualification or external ULPR review acceptance.

Reviewed exact consumer: `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`.
Reviewed exact fixture script SHA256: `71ee1e16efe3f9b1527da50af5f4fe8ac63ff9752e92d0fc7dad614483a8826f`.
The seven file digests are recorded in `frozen-v3/freeze-hashes.json`.

## Independent results

- Frozen fixture execution: **41/41**, rc 0, Python 3.11.17. Breakdown: 12 positive, 23 negative, 6 coverage boundaries. The independent JSON receipt is exactly equal to the author-provided receipt.
- Source-loader failure cases: **5/5 refused before fixture execution**, rc 2: wrong full pin, wrong path prefix, missing closure module, wrong blob SHA256, unavailable Git objects. The last case uses the real Git executable with an empty scratch object directory and no alternates; it does not mock the consumer or mutate the repository.
- Excerpt completeness regressions: **3/3 rejected**, rc 1/FAIL: empty params and beds, missing bed, missing h0. These same three cases incorrectly returned 41/41 PASS on v1. v3 fixes the issue by deriving the complete expected excerpt from fixed key sets and actual reader.BEDS instead of from the supplied contract's keys.
- Consumer regression mutants: **8/8 detected**. Each begins with verified bytes from the actual consumer pin, then changes one behavior in an isolated scratch source copy: rounded RESUME parsing, fallback past corrupt first S0, ignored S0 step, ignored atom step, removed gravity dispatch, ignored primitive history difference, missing-contact-column misclassification, raw CSV rewrite. These are review mutants, never certified as the pinned consumer.
- Original-input preservation: v3 asserts all supplied CSV/manifest/state hashes before and after read_run and checks retained windows as well as steps/events. A raw-file rewrite mutant fails all ten RESUME cases.
- Factual form comparison: only reference-pin fields changed; no previously null real input, registration, measurement, qualification or external verdict was populated.

## Findings resolved

1. A contract with missing scientific fields could certify itself by shrinking the expected comparison. The root reviewer identified the issue; this reviewer reproduced three counterexamples. The final fixed-key comparison rejects all three.
2. The initial RESUME fixture did not observe raw-file immutability or the returned window list. Those observations are now included, and the prose correctly distinguishes preserved source files from excluded returned rows.

## Scope accuracy and limits

The suite calls actual pinned consumer functions. It records G2's mass/rotation omissions, same-ID mass inventory limitations, gravity sensitivity, S0 candidate priority and step validation, observed G2c mismatch versus missing columns, primitive-floor history comparison and exact RESUME authentication. The status remains `physical_ready=false`, `P2_registration=null`, `physical_T12=NOT_RUN`, `research_runs_started=0`.

The new tests do not execute the entire restore/arm verdict flow or prove a real restart, raw inventory, R-a convergence, producer/consumer active definitions, actual binary/MPI behavior, h0 scaling registration, or a P2 implementation. The current document explicitly excludes r8 relabeling and h0 producer implementation from the 41 cases. Those are reasonable exclusions for this minimal preparation scope and remain physical/interface prerequisites.

The independent direct results are separate from the shared repository 155 checks. This reviewer neither ran a full gate nor changed shared-check/CI wiring. Root owns any subsequent full-tree check and Git operations.

## Evidence paths

- `frozen-v3-run.json`: exact independent baseline receipt.
- `loader-observations.json`: original v1 defect reproductions and source-loader checks.
- `loader-observations-v3.json`: final source-loader and excerpt regression results.
- `mutants-v3/report.json`: original source digests, mutant digests and detected case names.
- `reproduce_loader_checks.py`, `reproduce_consumer_mutants.py`: portable review-only reproduction scripts. `check_freeze.py` and `audit_mutants.py` preserve the original local runs.
- `review-plan.md`: initial independent source findings and physical boundaries.

All reviewer writes are inside `/workspace/.cloud-setup/t12-20261024/independent`. No checkout, main-tree file, Git ref, remote, real run, external application or physical data was changed.

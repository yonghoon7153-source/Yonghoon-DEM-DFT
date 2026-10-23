# Final integrated ULPR dump/restore evidence

All checks below used the integrated main-checkout sources, Python 3.11.17,
and fresh scratch copies. Source files were not modified. Both runs verified
their source hashes again at completion and reported `source_unchanged: true`.

| Check | Result |
|---|---:|
| Full `ul_gates.py --selftest` baseline | 202 / 202 pass |
| Full `ul_reader.py --selftest` baseline | 214 / 214 pass |
| Follow-up guard mutations | 10 / 10 killed by expected behavioral test failures |
| Unrelated or exception-shaped mutant failures | 0 |
| Independent review restore/UB probe | 12 / 12 expected outcomes |

Every mutant returned selftest rc 1, and all failed test names matched the
declared guard-specific pattern. The eight gates mutations each ran all 202
checks; the two reader mutations each ran all 214 checks. No test subset was
used. Exact failures and commands are in `mutations/results.json` and logs.

The independently authored probe was copied byte-for-byte as
`independent_restore_probe_original.py`. The wrapper adds provenance and result
assertions, without changing its 12 input cases. Baseline alone is
RESTORED / restore rc 0 / UB rc 0. The eleven altered-input cases all return
restore and UB rc 2: missing c26 is UNCONFIRMED; the others are VALUE_MISMATCH.
Results and original CLI logs are under `restore-probe/`.

## Exact source hashes (SHA-256)

| File | Hash |
|---|---|
| `ul_gates.py` | `c8d45a9cf75f0806e612d810942d23adea4b40feaa5f31f7d279eb8386358de6` |
| `ul_reader.py` | `34b46ebcf4530989917493f20d2d953043209e36d89e6b8282a2d629050a078d` |
| `ul_lib.py` | `23a79392352e01631c6d1f6aaecdb31fc8a53be518ee6f27b815896e161727e6` |

Both result JSON files record matching hashes for these and seven other
runtime/fixture source files. Their Git HEAD is context only: the tested
integrated changes were uncommitted, so file hashes identify the tested source.

## Reproduction

Use the configured Python environment and keep the four Python files together.
`--out` must name a new directory; earlier evidence is never overwritten.
`--repo` and `--kit` are accepted by both runners. `--kit` alone infers the
repository when it is under `REPO/docs/data`; otherwise also give `--repo` for
the immutable fixture archives and scripts.

```bash
python run_dump_mutations.py --repo /path/to/repo --out /tmp/ulpr-mutations-new
python run_dump_restore_probes.py --kit /path/to/repo/docs/data/ps45_unload_20261009 --out /tmp/ulpr-restore-new
```

These two argument forms were exercised in the recorded runs. Exact invocation
paths and interpreter version are in each result's `provenance.command` and
`provenance.python`. The helper copies the kit, links fixture dependencies for
read-only use, and deletes only its own temporary mirror after finishing.

## Boundary

This is implementation-side reproduction of independent probes and guard
mutation validation, not a replacement for the independent review or the full
repository gate (root handles that). It covers the ten BOX/header/G2c-time
guards added during review; it does not claim to rerun every earlier mutation.
Inputs are completed, stable dumps; concurrent file replacement and atomic
snapshot behavior are outside this check. No physical box/PBC values, material
parameters, actual simulation, external job, commit or push were performed.

# LHS release v1.1 independent review evidence

Pinned request snapshot: `8b3bc3d9c5632ec7db166a670f2a4ef156ba2077`.
Data/release commit: `c981d77f0`.

Start with `codex_lhs_release_final_verdict_20261001.md` (Korean verdict).

This package contains a read-only source subset in `snapshot/`, evidence in `evidence/`, and independent review scripts. It does not contain original LIGGGHTS dumps. Do not copy `snapshot/` over a working repository. Import only the verdict/evidence you need.

Reproduce in a Python environment with numpy, scipy, networkx and pandas:

```bash
export PYTHONDONTWRITEBYTECODE=1
python audit_release.py
python supplemental_probes.py
python final_evidence.py
```

On Windows use the equivalent environment-variable syntax. No DEM simulation is started by these scripts. Review outputs are written only under `evidence/` (tests use temporary synthetic fixtures).

- `audit_release.py`: all-row/all-column reconstruction, independent identities, HOLD/OK summaries and generator mutations.
- `supplemental_probes.py`: exact Git-blob verification, export mutations, real τ/ionic production-function counterexamples, eligibility rederivation and CLI byte reproduction.
- `final_evidence.py`: column appendix, null rules, supplemental tests. It includes two explicitly non-native test diagnostics: LF fixture writing and temporary symlink-to-copy replacement. Those are not equivalent to an unmodified Linux integration run.
- `run_baseline.py`: unmodified script selftests; see existing logs, including Windows-specific failures.
- `bootstrap.py` and `restore_source_bytes.py`: acquisition aids used during review, not needed for reproduction from this package. The former refers to other local snapshots; do not run it on receipt. The latter only repairs newline transport variants when exact pinned Git blob hashes match.
- `tree.json`: remote Git tree metadata used for byte validation, not an instruction source.

No production implementation, finding ledger, git checkout, simulation or external dataset was changed. The verdict distinguishes current frozen data acceptance from future pipeline hardening and physical validity.

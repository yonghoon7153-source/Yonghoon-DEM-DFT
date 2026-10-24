# Reproducing the independent T12 preparation review

The two review scripts take explicit input and output paths. They require Python 3 and local Git objects for the pinned ULPR commit. Neither fetches, changes refs, writes into the source checkout, or runs LIGGGHTS/MPI. Each output path must be new. If the configured cloud checkout uses an external Git object database, preserve its existing `GIT_ALTERNATE_OBJECT_DIRECTORIES` setting.

From the repository root, replace `/path/to/` with the location of these review scripts. The `--source .` argument points to the repository containing the frozen T12 fixture script and evidence JSON. These commands use actual local Git blobs from `--repo .`.

```bash
python3 -I /path/to/reproduce_loader_checks.py \
  --source . --repo . --output /tmp/t12-loader-independent
python3 -I /path/to/reproduce_consumer_mutants.py \
  --source . --repo . --output /tmp/t12-mutants-independent
```

Expected loader result: five source failures with rc 2, and three contract completeness failures with rc 1/FAIL; all eight review observations marked `pass=true`. Expected mutant result: all eight review observations marked `detected=true`. Both review scripts exit 0 only when every expected rejection/detection occurred. Their successful execution does not mean the altered consumer is valid: the source snapshot is hash-verified first, then deliberately changed only in scratch to challenge the fixture assertions.

The original v1 completeness defect is preserved in `loader-observations.json`; its three contract-shrinking cases incorrectly returned PASS. The fixed v3 observations are in `loader-observations-v3.json`. The portable scripts were separately rerun against the final v3 freeze, reproducing the successful outcomes without relying on hardcoded workspace paths.

The 41-case baseline is the existing fixture command documented in the T12 contract. These independent checks remain separate from the shared 155 repository checks and from physical qualification.

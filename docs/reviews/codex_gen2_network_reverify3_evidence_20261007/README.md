# Gen2 network reverify3 — review evidence

Pinned source: 0801d4ceb540f5a5813761b20a5e0f304ed80a03 (2026-10-07).
Read `codex_review_gen2_network_reverify3_20261007.md` first.

This is NOT a production release, a 194 batch result, or an S3 campaign.
The release_gate output directories are deliberately synthetic gate experiments.
Their embedded old-data/g2 labels and TEST_ONLY_NOT_A_GO.md must NOT be handed to ML.

## Contents

- source/: 432 exact pinned Git blobs, selected dependencies/tests/fixtures; not a full git checkout.
- source_manifest.json: commit, Git blob SHA-1, SHA-256, length for every source file.
- submitted/: exact user attachments (text matches pin).
- probes/: independent old and new probes.
- evidence/: saved JSON, raw stdout/stderr, synthetic fixtures and gate outputs.
- verify_evidence.py: source-byte and review-result assertions; 22/22 includes assertions that current defects REPRODUCE.
- run_tests.py: selected original tests. Not all tests are expected to pass without full Git history / historical corpus.
- run_probes.py: evidence reproduction harness.
- prepare_source.py/source_plan.json/extra_plan.json: acquisition bookkeeping, not needed to reproduce probes.

## Reproduction

Use a fresh unpacked copy. Python 3.12 + numpy 2.5.3, scipy 1.16.3, networkx 3.7, Flask, matplotlib 3.11.2 and the project test dependencies.
Dependencies themselves are excluded. The wrappers also look for this workstation's sibling/local deps directories;
if they are absent, normal Python site-packages are used. TMP is inside this evidence folder.

```bash
python run_probes.py acceptance branch_policy dependency_gap input_digest
python run_probes.py seal_paths
python run_probes.py new_gates release_gate scope_checks
python verify_evidence.py

python run_tests.py test_gen2_publication_handover test_gen2_role_contract g2_network_reread
```

No command above launches production194. S3 scope_checks invokes only a tiny synthetic run_case fixture.
seal_paths creates synthetic manifests/records and invokes audit/reread, not run/retry workers.

## Qualifications

- release_gate patches only the upstream tau rereader, equally for good and bad cases. Actual build/check and evidence gate are untouched.
- scope_checks uses a Git-read adapter populated from independently verified pinned bytes; no claim of native Git subprocess verification.
- Historical audit admission has NO_RECORD 194 in the isolated fixture, not 194 numerical verification.
- Successful admission of a failed row as blank is not admission of its rejected numeric payload.
- Actual WSL raw files, real preflight and production194 were not run.
- Existing failed/SKIP test logs are retained; no all-green claim.
- A repeated scope_checks probe initially stopped because its synthetic raw fixture directory already existed. The reviewer harness now allocates a unique directory per replay; the subsequent replay succeeded. This was a reviewer-harness issue, not a product finding. The earlier attempt record is retained.

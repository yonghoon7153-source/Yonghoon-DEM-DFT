# Gate66 reviewer evidence

Primary result: `GATE66_REVIEW_KO.md`; forwardable response: `CLAUDE_REPLY.md`.

Target HEAD: fa947cc9b17cdbeffbb39447c99159bc2c831e6e.
Review environment: Windows, CPython 3.12.14. No Linux kernel success claimed.
No production edits, registry restoration/deletion, science runs, push or PR.

## Evidence layout

- `*.json`, `*.stdout.bin`, `*.stderr.bin`, `*.xml`: command records and raw outputs. `.bin` outputs are text bytes, retained without newline normalization.
- `startup_cases/`: seven unmodified production receipt-function cases with a small replay cwd.
- `startup_fullsandbox/`: four cases using production `_make_sandbox()` copies. Sandbox paths in receipts are review-host paths, not bundled repositories.
- `partial_mutations/`: supplemental registered-mutant checks using `--noconftest`. Four match full expected fail/witness sets. E2-R has two static failures and one native skip; it is not complete.
- `registry-audit.json`: all 175 deleted tracked records, old content/hash and aggregate counts.
- `TARGET_IDENTITY.json`: target/input file hashes and git/status observations.
- `MANIFEST.json`: delivery payload hashes. This is review-package integrity, not independent attestation of native Linux replay.

## Portable primary repro

Use a checkout at the fixed HEAD and an available Python with the project review dependencies. The fixture needs an interpreter without a system sitecustomize to expose the cwd-only case. Native controls record that premise; do not infer it.

```text
python repro_startup.py --repo /absolute/checkout/degradation-degeneracy --out /new/empty-output --full-sandbox --case plain --case cwd_only_candidate --case cwd_on_pythonpath --case remove_loaded_path
```

The output directory must not already exist. Full sandbox copies remain for inspection. Original files are not changed. The script must be run with the intended interpreter; it uses `sys.executable` for children.

For T1, from the target subtree:

```text
PYTHONNOUSERSITE=1 python -m pytest tests/test_gate65_defensive.py --noconftest -q -p no:cacheprovider -k the_interpreter_fixture_measures_its_own_premise
```

The environment assignment shown is POSIX syntax. On Windows use an explicit subprocess environment, as in `run_checks.py premise_env_disabled`. Expected current result: 1 failed, 1 passed, 15 deselected. Remove only that variable for the contrast. The fixture creation is a diagnostic, not a production setting change.

`run_checks.py`, `audit_registry.py`, `partial_mutations.py` retain the actual review workspace defaults. To use those convenience runners elsewhere, adjust only their ROOT/REPO/PY/HERE defaults or issue the recorded command with your paths. The primary startup repro already exposes `--repo` and `--out`.

Git-only registry reproduction requires both fixed revisions (fetch history if using a shallow clone):

```text
git diff --name-status --diff-filter=D 5e4cf1038f0f26a6a624d9984386cfd046657ac3 fa947cc9b17cdbeffbb39447c99159bc2c831e6e -- degradation-degeneracy/docs/22p_gap/_exec_class
git show --format= --numstat d60f25391f9e7a08c210ef559efa0d58589171be -- degradation-degeneracy/docs/22p_gap/_exec_class
```

No saved virtual environments, generated pytest temp trees, disposable whole repositories, Git credentials, or ignored science results are in the delivery ZIP. Files contain ordinary local review paths. No external transmission was performed.

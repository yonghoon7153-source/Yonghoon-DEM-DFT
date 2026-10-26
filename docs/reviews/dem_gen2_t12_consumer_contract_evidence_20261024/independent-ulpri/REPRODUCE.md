# Independent T12 successor checks

Use Python3 with `-I` and existing local Git objects for published consumer `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`. Preserve any configured alternate object database. These scripts only create new scratch output directories; they do not fetch, mutate Git or run physical calculations.

```
python3 -I /path/to/reproduce_loader_checks.py --source /path/to/frozen-T12 --repo /path/to/repository --output /new/scratch/loader
python3 -I /path/to/reproduce_consumer_mutants.py --source /path/to/frozen-T12 --repo /path/to/repository --output /new/scratch/mutants
```

The source root contains `scripts/test_dem_gen2_t12_consumer_contract.py` and its source-manifest/contract JSON under the committed evidence directory. Run the ordinary fixture command separately for the direct52 receipt.

Expected loader result: five source failures with rc2 and three completeness failures with rc1/FAIL, eight observations `pass=true`. Expected mutation result:13 observations `detected=true`. Each mutation starts with hash-verified consumer blobs, changes only scratch, then requires a completed52-case result and specific named semantic failures. Interpreter crashes do not count as detection.

The original eight mutants cover integer rounding, corrupt-first S0 fallback, requested S0/atom step, gravity dispatch, history comparison, missing contact classification and raw input rewriting. Five new mutants remove event preflight, ignore its problems during authorization, remove the manifest separator guard, select the manifest key before that guard, or normalize raw event lines using splitlines. The final normalization mutant is caught by the single leading LS fixture, demonstrating why an extra valid RESUME event is not required to expose the defect.

Results remain separate from shared155 and physical qualification. External ULPRI integrity HOLD awaits external recheck. G2 mass/omega equivalence and P2 readiness are not established. Old41 and pre-fix44/52 evidence remain historical; cancelled old fullgate130 is not a PASS.

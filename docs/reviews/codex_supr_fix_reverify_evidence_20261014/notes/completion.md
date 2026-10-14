# SUPR-02 completion review notes

Pin: `df647d4e31224e1a270dae01dd41f91af3048361`. Scope: runner completion capture/P0–P10 and supplementary receipt consumption; no production run, source edits, or Git writes.

Conclusion: no new valid false positive or material overblocking found in this completion scope. SUPR-02's prior truncation/missing-prerequisite acceptance is closed, subject to the external-authenticity and launch-approval qualifications already stated in the request.

## Independent evidence

`probes/completion_probe.py` produced 40 cases with no unexpected result. `evidence/completion_probe/results.json` preserves the results and each case's JSON/log. Run from this review directory with bundled Python `-X utf8 -B probes/completion_probe.py`; the probe deliberately refuses overwriting an existing normal evidence record. Use a fresh review directory for a second capture.

Environment-only preflight data and Windows POSIX guard are synthetic. Real functions used: plan construction, `plan_input_digest`, `production_observation_problem`, `print_preflight`, actual dry-run dispatch/capture/receipt creation, P0–P10 verification, and supplementary receipt consumption. Therefore this is evidence about completion recording and verification, not WSL raw-file availability, actual import execution, or numerical validation.

| Probe | Result |
|---|---|
| Normal registered supp20 dry-run, real captured receipt/log | Producer rc=0; P0–P10 pass; supplementary receipt rc=0; ROOT not created |
| Missing/false/nonboolean completed; missing/nonzero/string/float/bool exit_code | P3 rejects all |
| Exception, nonempty stop, omitted stop, aborted | P3 rejects all |
| False observation in record, args, or parsed argv | P4 rejects; P6 also catches args/argv disagreement |
| Missing prerequisite record, `ok=1` instead of literal true | P5 rejects |
| Prefix before completion marker | P1/P3 reject with unchanged binding; P3 rejects after rebinding hash/bytes |
| Three prerequisite lines removed | P1/P5 reject with unchanged binding; P5 rejects after rebinding |
| Duplicate marker, content after marker, stop text before marker | P3 rejects |
| Missing machine digest line | P2 rejects |
| One byte appended without rebinding | P1 rejects |
| Actual observation-OFF dry-run | Producer rc=2; P3/P4 reject; supplementary receipt rc=1 |
| Same OFF log truncated before first stop line | P3/P4 reject |
| Producer supplied missing dependency/lazy/fork preflight fields | Each prints failure and is rejected by P5, even though deliberately malformed synthetic preflight omits its stop reason |
| RuntimeError, KeyboardInterrupt, SystemExit injected after original cmd_run reaches completion marker | Captured exception; completed false; P3 rejects all |
| Unknown cohort raises LaunchError | Producer records rc=2 and incomplete receipt; verifier rejects |
| Original pair relocated, original absolute log path unavailable | Sibling log fallback passes |

The supplementary consumer was directly checked on normal, observation OFF, rebound truncation and rebound missing-prerequisite inputs; results respectively 0, 1, 1, 1.

## Original selftest environment diagnosis

The unchanged supplementary receipt selftest initially returns **79/88**, with nine normal/variant assertions failing because generation derivation fails. `derive_generation(ROOT)`'s isolated subprocess cannot import `scipy` in the bundled Python. It records `generation=null`, and the actual preflight stops with rc=2; P3/P8 correctly reject that receipt. Captured original positive fixture is under `evidence/completion_environment/original/`.

`probes/completion_environment.py` reruns the same source and selftest, intercepting only the exact `python -I -B -c GEN_PROBE` child command to prepend two existing dependency directories to its `sys.path`. It does **not** substitute the probe or generation result. The real probe returns `generation=g2`, `g2_name=g2`, modes `hertz/physics/hertz_h12`, and no problems. With only that dependency bootstrap, the unchanged selftest returns **88/88, rc=0**. The full actual preflight therefore passes after this environment dependency is supplied; the earlier 40-case mock does not mask an observed normal-path receipt failure.

The selftest retains its documented raw-file/POSIX/git mocks and cached real generation/dependency analysis. Wrapper, bootstrap text, real failed/successful probe results, both full selftest logs, and both normal receipt/log captures are retained in `evidence/completion_environment/`. A sandbox default-temp permission failure was resolved by setting the review harness's temporary directory inside that evidence directory; no source changes or dependency installation occurred.

## Source anchors

- `scripts/run_network_194_parallel.py:1809–1825`: missing/malformed prerequisite data yields explicit false values; the display and receipt share the predicate.
- `:1960–1984`: output-byte count and SHA binding, with relocation fallback.
- `:1996–2018`: literal completion, integer rc=0 excluding bool, no exception/stop/abort, exactly one final completion marker; observation ON and three explicit successful prerequisites.
- `:2020–2085`: argv, code/digest, generation/raw, plan and optional approved-pin comparisons.
- `:2650–2663`: stops return 2 before completion; dry-run completion marker and state are set immediately before rc=0.
- `:2739–2768`: receipt uses same run state/output, records argv/args, output hash, completion, exit, exception and runner fingerprint.
- `:2775–2817`: requires dry-run, fresh paths outside ROOT; catches stop/error states, writes log before JSON, propagates unexpected exceptions.
- `scripts/supp20_input_receipt.py:350–360`: standalone text rejected at E0; every runner check is incorporated.

## Qualifications, not new SUPR-02 defects

`runner.sha256` is recorded at runner line 2753 but is not compared by P0–P10. Removing `runner` or changing only its hash still passes; this is an explicit additional probe. P7's identity comparison covers the numeric sealed files, and P10 covers the supplied approved SHA; neither is an external attestation of the runner file. Preserve the prior §6 qualification to inspect final-pin tool changes and retain tool fingerprints. Do not describe P0–P10 as automatically authenticating every execution-tool hash.

Likewise `--approved-sha` is optional with a warning, and a coherent malicious fabrication of both receipt and log is explicitly outside the request. No such forgery is counted as a new acceptance defect. Normal receipt generation retained the required provenance fields; this review did not prove atomicity across two files against concurrent hostile writers or external storage failure.

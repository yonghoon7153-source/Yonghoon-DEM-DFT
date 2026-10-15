# Q2 / Q3 independent review — receipts and IDs

Pinned source: `eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84`.
Probe: `probes/receipt_ids_recheck.py`; result: `evidence/receipt_ids_recheck.json`.
Actual production functions and unchanged CLI commands were run against synthetic files. No Bash runner, MPI, LIGGGHTS, simulation, Git mutation, source edit, or real experiment occurred. The old independent review's restoration baseline constructor is loaded as definitions only; its prior tests do not execute. Arm serialization uses the kit's fixture writer, with independent mutations and actual reader/selection/gate calls.

Delivery is self-contained: the old baseline definition is included in `support/previous_restore_baseline.py`, with original-file SHA256 provenance; the probe reads this review's `evidence/history_reread.json` for the existing actual H0–H5 evidence. No sibling review directory is required.

Result: 92 asserted checks, 90 satisfied. The two unsatisfied checks are one defect: missing G2c reference-column headers still raise `KeyError`. Five additional scope observations are intentionally not counted as passing or failing assertions.

## Q2 — original ULKRR-03 receipt defect is fixed, but the broad claim needs a scope qualification

`ul_reader.py:992–1024` now rejects missing, noninteger, nonzero, and duplicate `fails` or `reader_rc` fields in the last end record; missing `grammar_prereq=PASS` also blocks RESTORED reuse. `gate('RJ2')` at `ul_reader.py:1050–1057` consumes the EXT receipt as requested. Independent positive controls pass. Failed/missing/duplicate receipt cases refuse UB and RJ2.

The exact prior process-level counterexample is closed. On complete independent R/UN/UK evidence, the unchanged restore CLI and unchanged kebase CLI both publish their outputs and then exit 120 when stdout is closed. The runner-equivalent aggregate record is `end=x fails=0 reader_rc=2`. The new gate refuses UB. The fixture does not install a fake RESTORED certificate or fake KE baseline: both are issued by the actual commands. See case `actual_restore_stdout_failure`.

The question's intentional omission of arm receipts is observable, not an inference:

| Case | Actual freshly recomputed result | Downstream result |
| --- | --- | --- |
| Valid UT; actual arm CLI publishes then exits 120 on closed stdout | UT `primary=OK`, `trajectory=RM_STOP`; its `_job_receipt` is false | `selection=need_UV`, UVa allowed |
| Same complete valid observations; append synthetic late screen ERROR, FAIL rc1 stage check, and fails1 receipt | UT `primary=OK`, `trajectory=RM_STOP`; receipt false | UVa allowed |
| Same arm while its end receipt is absent | UT `primary=OK` | UVa allowed |
| Valid UVa observations with `fails=1 reader_rc=120` | Selection resolved t1 | Other-bed UB and 7:3 G_UB allowed |

Relevant source: `_arm_v` `ul_reader.py:971–978`, `selection_state:980–989`, gate branches `:1072–1108`, and `report:1596–1608`. `arm_verdict:627–896` reparses observations and thermo but does not consume the arm job receipt or its run_check technical status. `run_unload.sh:300–305` can record nonzero FAILS/RRC after creating the observations and reader outputs.

Interpretation: “do not reuse a failed RJ/RJ2/EXT issued certificate” is supported. “No output of any technically failed job can authorize later work” is not supported by the implementation. Recomputing protects against a stale or incorrect `arm_verdict.json`, but it does not establish process completion or absence of simulator technical errors. The actual stdout failure does **not** prove the numerical observations are wrong. A late stage failure does **not** prove earlier completed primary observations are wrong either; primary-value retention after incomplete auxiliary work is an existing design choice. Therefore these observations should not be inflated into a new numerical P1 or into evidence that all earlier fixes are invalid. Either state the exception explicitly and accept fresh re-evaluation of valid arm observations, or require the latest arm receipt before dependent submission while retaining the valid primary measurement for reporting. This is the precise remaining Q2 policy choice.

No attack that rewrites all provenance was needed. The stdout case uses actual unmodified Python failure; the late stage case is a synthetic failure after valid observations, not a real simulator execution. Receipt-only UV mutation is disclosed as a scope probe, not claimed as observed scheduler behavior.

## Q3 — normal ID fixes pass; one parser-error path remains

Passed independent paths:

- PRE, POST, R_END, UN: fractional, zero, negative, NaN, infinity, and missing `id` header all yield a structured non-RESTORED result and UB refusal.
- Original S0: fractional, zero, negative, and missing `id` header all refuse restoration without an exception.
- Endpoint atom frame: fractional, zero, negative, and missing header all produce UNIDENTIFIED and UVa refusal.
- S3 contact dump: both reference fields reject fractional IDs and renamed required headers without an exception.
- Direct `s3_residual`: atom ID and both pair reference IDs reject fraction/zero/negative/bool/string/over-limit integer, with NOT_COMPUTED and no exception.
- G2c pair IDs: both reference fields reject fractional/zero/negative IDs without an exception.
- The unchanged G2 token parser rejects fractional lexical IDs with `int(token)` rather than truncating float values; its caller catches `ValueError` (`ul_gates.py:215–236`).

### Residual P2 candidate: G2c reads required keys before respecting a parser error

Location: `ul_gates.py:252–256`, invoked by `g2c_compare:287` and `ul_reader.restore_verdict:1335`.

On the positive complete restoration fixture, change only the test contact-dump header `c_cpl[7]` to `not_c_cpl[7]`. Leave every numeric row and other file unchanged. `read_dump` records the required-column mismatch and returns `ok=False`, but `_contacts` immediately executes:

```python
for r in d['rows']:
    v = [r[f'c_cpl[{i}]'] for i in range(1, 27)]
```

The result is `KeyError('c_cpl[7]')` from both actual `g2c_compare` and actual `restore_verdict`. The equivalent mutation of `c_cpl[8]` reproduces the same issue. Cases `g2c_c_cpl7_missing` and `g2c_c_cpl8_missing` retain the mutated files and function outcomes.

The actual unchanged restore CLI reproduces rc1 with the full traceback (`g2c_missing_column_actual_cli`). It does not publish a certificate, and UB is refused. Thus this is a structured-failure/reporting defect, not a false RESTORED or false U authorization. It is the same class as the previous missing-column KeyError part of ULKRR-04, in the G2c path newly claimed by Q3. A `d['ok']` early return before key access would allow `g2c_compare` to return its already-designed FAIL+reason result. This review does not implement that change.

### Precision boundary: nonblocking limitation of the word “exact”

`read_dump` converts all tokens to float (`ul_lib.py:364`) before `exact_id` checks them (`:468–475`). The raw integer token `9007199254740993` becomes `9007199254740992.0` and is accepted at the inclusive 2^53 bound. The decimal token `1.0000000000000001` likewise becomes 1.0 and is accepted. The next representable value `9007199254740994` is refused, and ordinary 1.5 is refused.

This establishes only that the new helper guarantees integral *parsed float values*, not exact integer *lexemes*. The current beds are nowhere near 2^53 particles; this review has no realistic production failure from that boundary and does not count it as a release blocker. If lexical exactness is intended, preserve/parse ID tokens before converting to binary float. It is not appropriate to multiply this into findings for every consumer.

## Reproduction and interpretation of exit code

From the review folder:

```text
python -X utf8 -B probes/receipt_ids_recheck.py
```

The script's rc0 means it completed and wrote the evidence. Read `summary.failed_expectations`, not just the process exit code. Positive controls are asserted before the associated mutations. Each run gets a new `evidence/receipt_ids_cases_*` directory; the result JSON identifies the active one and hashes the pinned source files. Prior run directories are retained.

# R11 data-contract / scientific-boundary subreview

Target: `bms-balancing/` at evidence commit `2add074cf0c3ebfaa02b22d2311dd4330f0879b0`; executable code is unchanged from `665c87e1`.

Verdict for this subreview: **NO-GO — P1 × 5, P2 × 2.** These are new false-promotion, false-canonical, or wrong-GO paths. This report does not count the already-declared general export gap, typed `(root,state,si)` gap, or pending U18 measurement as findings.

Reproducer: `outputs/r11_data_contract_repros.py`  
Captured results: `outputs/r11_data_contract_results.json`

The numerical solver and file writer are deterministic fakes only in the two roster producer probes; the reviewed roster construction, status decision, canonical/partial destination choice, checker, schema, production reader, and shell wrapper are the target code itself. All target inputs are temporary. The target worktree remained clean.

## P1-1 — Promotion is not bound to baseline input bytes

**Code:** `bms_balancing/schema.py:51-52,128-164`; `scripts/check_u14.py:44-49,244-258,479-490`.

**State / command:** create separately signed baseline/candidate `matrix_100.csv` units with the same row keys, science numbers, controls, environment, and run id. Give each side valid four-role target and reference receipts, but change every SHA/digest. Run:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case receipt_identity
```

**Observed:** target digest `9d6ace08c3d4 → 48cf03a6b6b8`, reference digest `d789ce826bcd → e9a7ac3dea7c`; all four differ. `check_u14.py` returned `0`, printed “전부 같다”, all `blocked_by` counts were zero, and emitted `"promotion_eligible": true`.

`validate_receipt` proves only that each receipt is self-consistent. `ROW_SKIP` then removes `inputs_sha`, `ref_inputs_sha`, `consumed_inputs`, and `ref_consumed_inputs` from old↔new comparison. Thus “same execution” accepts a wholly different dataset when the compared outputs happen to agree (for example, changed unused workbook cells are enough).

**Minimal fix:** after validating each receipt, normalize both target and reference to exact `{logical_role: sha256}` maps and compare candidate to baseline. Treat any byte-identity change as an input/control mismatch in `blocked_by`, before numeric equality. Keep path out of scientific equivalence if byte-identical copies are intentionally equivalent; do not omit byte identity itself.

## P1-2 — A negative allowlist silently defeats a newly present measurement

**Code:** `bms_balancing/data.py:30-36,58-65`; `bms_balancing/verify.py:1445-1456,1505-1508,1581-1586`.

**State / command:** place both `data/half_cell/GITT/300_0147.xlsx` and `data/half_cell/step_005C/300_0147_005C.xlsx` in the data root, then execute the production matrix roster/status path:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case allowlist
```

**Observed:** both files existed during the run. `D.declared_states("GITT")` still returned only `100, 200, 300_0009`. Matrix skipped GITT before checking existence, requested 16 step-only combinations rather than the on-disk 32, reported `status:"complete"`, wrote the canonical `matrix_300_0147.csv`, and returned `0`.

The issue is not that absence must be inferred from existence. It is that an old negative declaration wins silently when current data contradicts it.

**Minimal fix:** bind the absence declaration to a versioned data-side manifest/dataset identity. At minimum, treat “allowlisted absent path now exists” as a hard declaration/data conflict (`invalid`, rc 2) until the manifest is deliberately updated; never silently subtract a present pair from canonical authority.

## P1-3 — Matrix diagnostic switches redefine the authority and still publish canonical

**Code:** `bms_balancing/verify.py:1445-1456,1505-1508,1581-1586,1924-1925`.

**State / command:** both GITT and step-005C state-100 files exist; invoke the matrix production path with `only_source=true` and `only_wdqdv=true`:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case matrix_subset
```

**Observed:** the complete scientific matrix authority is `2 sources × 8 Si × 2 weights = 32` rows. The switches first narrowed `sources` and `weights`, after which that eight-row request became its own authority: `status:"complete"`, canonical write, rc 0.

This is the matrix analogue of the R10 `ne_shape --states` bug: the caller can narrow the population before completeness is judged.

**Minimal fix:** construct the fixed canonical matrix authority before applying diagnostic selectors. Any selector that narrows it must yield typed `subset`, rc 3, and a run-id-scoped partial destination (or reject canonical `--out`). Seal the exact requested tuple roster, not only its count.

## P1-4 — `--grid 1` is a one-point profile declared complete

**Code:** `bms_balancing/verify.py:1612,1683-1690,1725-1736,1926`.

**State / command:** run the production profile roster/status path with `grid=1`:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case profile_grid
```

**Observed:** `np.linspace` created one γ (the lower bound). The self-declared roster was `{requested:1,succeeded:1,missing:[]}`; profile reported `complete`, wrote the canonical profile, returned 0, and reported every within-tolerance scientific span as `0.0`. The production wrapper's intended canonical grid is 21.

R10 sealed failures relative to the requested grid, but the caller still defines that grid. A one-point search therefore “proves” a zero-width profile.

**Minimal fix:** define and sign an authoritative canonical γ grid (including exact values/config version). Noncanonical `--grid` is diagnostic/subset: rc 3 and partial namespace. Never derive canonical completeness solely from the caller-selected grid.

## P1-5 — The scientific reader consumes a row the shared validator calls an error

**Code:** `bms_balancing/schema.py:167-208`; `scripts/ne_shape.py:108-147`.

**State / command:** make a correctly unit-signed matrix with one `(GITT,Li,0)` row containing `gamma_Si=0.4`, `ref_gamma_Si=0.2`, and `error="optimizer failed"`. Run:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case shape_reader
```

**Observed:** `S.check_rows("matrix", ...)` rejected the unit as “`error` row 1/1 — success 아님”. Production `ne_shape.fitted_pair_info`, which only verifies the unit signature and duplicate key, returned that same row's `(0.4,0.2)` pair for scientific inference.

This is not the closed U18 checker bypass: the checker now rejects correctly, while the production consumer does not call it. The claimed shared typed boundary is split at the reader.

**Minimal fix:** in `fitted_pair_info`, run `S.check_rows("matrix", rows, exact_header)` and reject on any problem before key selection. Then require the selected row's receipt/control cohort to be compatible with the current shape run; a signature proves integrity, not scientific eligibility.

## P2-1 — `shape_step` reads stale namespace state and the outer wrapper turns partial into success

**Code:** `scripts/run_states.sh:211-236,297-317`.

**State / command:** partial namespace contains fresh `ne_shape_Z_Li.csv` with status `partial`; root contains stale `ne_shape_A_Li.csv` with status `complete`; child returns 3. Execute the exact extracted production `shape_step` and outer case mapping:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case shape_wrapper
```

**Observed:** `shape_step` used namespace-wide `ls ... | head -1`, preferred stale canonical for the status read, and printed `부분(complete)` while pointing at the fresh partial file. It propagated `SHAPE_RC=3`, but the outer wrapper left `FAIL_COUNT=0`, printed `전부 통과`, and exited 0.

**Minimal fix:** have the producer return an exact attempt manifest/path; never rediscover its result with a wildcard. Require `rc ↔ meta.status ↔ exact artifact` consistency. Preserve rc 3 (or another non-GO aggregate result) at the top level; it must not become “all passed”/0.

## P2-2 — Receipt paths and flattened role cardinality are unauthenticated semantics

**Code:** `bms_balancing/schema.py:58-86,128-164`.

**State / command:** swap `full_cell.path` and `half_cell.path` while leaving role-bound SHA values unchanged; separately provide both nested `literature.gr` and a conflicting direct `"literature.gr"` leaf. Run:

```text
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case receipt_shape
```

**Observed:** the path swap kept the same aggregate digest and `validate_receipt` returned no problems. The duplicate flattened role produced five leaves including `literature.gr` twice with conflicting SHAs, yet the set-based required-role check and recomputed digest also returned no problems.

**Minimal fix:** use one exact typed receipt shape, recursively reject unknown/nonleaf structures, prohibit ambiguous dotted-key flattening, and enforce every required role occurs exactly once. Keep a path-neutral execution digest if “same bytes = same execution” is desired, but bind a normalized logical locator/path in a separate receipt-integrity field and validate that each recorded SHA was taken from that snapshot. Path neutrality and path authenticity are different contracts.

## Answers to the R11 design questions in this scope

1. **Digest/path:** do not discard the useful “same bytes may be relocated” premise. First fix the more fundamental bug: compare role-bound SHA maps baseline↔candidate. Preserve the content/execution digest as `(role,sha)`, and separately bind typed logical locators/path claims. Reject duplicate flattened roles.
2. **Known absence:** a negative roster assertion belongs with the versioned dataset manifest. A code default is acceptable only if it is checked against the selected dataset and a present supposedly-absent file is a hard conflict.
3. **Export scope:** enforce one snapshot for shared full-cell and literature roles. Half-cell files are legitimately state-specific, so bind them as `(source,state,sha)` rather than forcing target and pristine to be the same file. Derived cross-state consumers also need a batch/cohort manifest for the exact matrix units they aggregate.
5. **Partial lifetime:** current behavior is insufficient. Use immutable `partial/<producer>/<attempt-or-batch-id>/...` units plus an explicit retention policy/index. Never let a later partial silently overwrite the evidence for an earlier one, and never select an attempt via `ls | head`.

Question 4 (evidence-tool sealing) is outside this data-contract subreview.

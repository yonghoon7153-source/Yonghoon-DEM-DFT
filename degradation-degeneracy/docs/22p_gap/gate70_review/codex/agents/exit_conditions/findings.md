# GATE70 E1 / E2 / E4 independent review

Reviewed read-only repository: `C:/Users/Administrator/Documents/Codex/g70_20260924`.
Observed HEAD: `8568f782db3acbf00d872ce5527147258c00bec7`.
Requested code target: `f0dfaff3bea1e1caedcd7a34275e908284cc2d4f`.
`git status --short` returned no entries. `git diff <code-target> HEAD -- degradation-degeneracy/src degradation-degeneracy/tools degradation-degeneracy/configs degradation-degeneracy/scripts degradation-degeneracy/run.sh` returned no changes. This subreview did not independently recompute source_digest.

All line references below are at the observed HEAD and relative to `degradation-degeneracy/`. No repository edits, numerical solves, COMSOL, migrations, restoration, or class changes were performed. Conclusions below are static audit findings, not claims of freshly rerun tests.

## Proposed classification

| Condition | Actual current status | Classification for the proposed cooperative canonical grid/fit calculation | What remains unproved |
|---|---|---|---|
| E1 | Open for the original projection producer contract. The E1 proposed repair names a different artifact/tool. | Result/evidence limitation unless the requested result also claims independently producer-bound cohort projections. No path from this missing producer receipt to wrong grid/fit numerical output was established. | The supplied projection/restart payloads actually came from the declared producer, with their typed manifest and payload digests bound together. |
| E2 | Open. Existing source hashing is measurement by the running code, not an independent launcher outside the measured source. | Result/evidence limitation for this run under the already documented deployment assumptions. It blocks a stronger independently attested runtime-code claim. No new in-scope numerical corruption was established. | The bytes actually executed, including relevant startup/import behavior, are independently bound to the run. |
| E4 | Open. The coverage checker validates submitted reports and derives their verdict; it does not rerun their mutation scenarios. | Review-evidence limitation; not a direct grid/fit execution prerequisite. It blocks a claim of independently replayed mutation coverage. | Submitted scenario outcomes were independently reproduced on the reviewed code/environment. |

This classification is an explicit narrowing of the assurance claimed for a conditional run, not closure of the older requirements. `docs/08_REVIEW_RESPONSE.md:7087-7091` keeps these independent GO preconditions open, and `:7105` asks for their implementation plus fixed-commit, whole-process/environment regression. `docs/22p_gap/STAGE3_CONTRACT.md:1252-1258` explicitly says that independent replay and trusted launcher cannot be removed as deployment assumptions without weakening the claim. Conversely, the historical label P0 does not by itself establish that today's grid/fit results will be wrong. Existing limitations should not be counted as fresh P0 findings.

The applicable deployment boundary is already documented, not invented here: `STAGE3_CONTRACT.md:1227-1235` records one principal, local ext4, accidental pipeline interference, and requires remeasurement if deployment changes. `:1240-1249` keeps public API behavior and import-node measurement defects in scope; noncooperating direct same-principal writers and ineffective cross-system locking are outside that boundary. This review does not require a new adversarial security boundary.

## E1: original producer condition differs from the proposed archive repair

Historical requirement: `docs/22p_gap/GATE49_REQUEST.md:16` names the tuple `(leg, producer identity, manifest digest, projection digest, restart digest)` and two decompressed payloads. This is the projection producer contract, not a generic fit archive manifest.

Current producer implementation:

- `docs/22p_gap/row_projection.py:2401-2410` creates `<leg>.restarts.csv.gz` and `<leg>.projection.csv.gz`.
- `:2483-2495` writes their manifest with leg, projection schema, both payload hashes, analysis spec and analyzer identity.
- `:3544-3576`, `assert_producer_binding`, parses a YAML document and only checks the supplied `analyzer.producer_semantic_sha256` against the ledger pin. It does not implement a closed manifest schema, decompress/re-hash these payloads, or verify a producer-issued receipt binding the full tuple.
- Reader path `:3529-3540` verifies generation member bytes against CURRENT and then calls this producer check. Whole-file integrity is not proof of the declared producer's generation of those contents.

The proposed E1 closure at `GATE70_REQUEST.md:34` changes `tools/archive_bundle.py`. Its present artifact is different: `tools/archive_bundle.py:297-301` writes `restore_map.yaml` and `payload_sha256.yaml`; `:369-377` already hashes all bundle members; `:384-390` checks a fit start-attempt manifest. Doing only that proposed archive repair would not close the old projection/restart producer condition.

One proposed regression also needs precision. `row_projection.py:2405-2408` explicitly makes the uncompressed digest the canonical anchor because compressor implementations can yield different gzip bytes. Recompression of identical uncompressed data should not automatically become a producer-contract failure. Reject changed decompressed content or broken envelope bindings; treat compressed transport-byte identity as a separate check if declared.

Minimum closure evidence:

1. Identify the actual projection publisher/reader consumers covered by the condition; implement the check there, not merely in the unrelated archive tool.
2. Parse a closed typed projection manifest and validate the leg, producer identity, schema/spec, and exact expected payload identities.
3. Recompute both decompressed payload hashes and bind them, with the manifest digest and leg, into a producer-issued receipt verified by the consumer.
4. Demonstrate the positive genuine-producer path plus rejection of altered manifest identity, substituted/missing projection or restart payload, and receipt/manifests from another leg or producer. Preserve the declared meaning of uncompressed hashes across benign recompression.

While open, state that cohort projection producer attribution is not independently verified. Do not describe this as a demonstrated failure of the grid/fit numerical calculation, and do not claim E1 closed by an archive checksum change alone.

## E2: runtime-code attribution remains self-measured

`src/io.py:194-229` computes `source_digest` from disk files beneath the root derived from its own `__file__`, including the RUN_SCOPE paths. It is not a trusted launcher measuring actual executed code outside the measured program. The grid/fit paths call this helper (`src/grid.py:265,367,446`; `src/fitting.py:865,908,1144,1484,1643`). They provide valuable source consistency evidence without independently proving imported execution identity.

For the projection producer, `row_projection.py:2189-2192` measures source read from `_producer_source_files`; `:2213-2223` derives its locations; `:2226-2248` writes self-reported analyzer provenance. The earlier decoy-specific repair moved `_producer_source_files` inside the semantic identity boundary (`:391-397`; documented in `GATE54_REQUEST.md:49`). The existing regression at `tests/test_docs_lint.py:10986-11002` asserts it is no longer in `_PRODUCER_CUT`. That resolves the earlier excluded-selector defect, not the distinct launcher trust boundary. I did not rerun that historical decoy probe.

`GATE54_REQUEST.md:12` and `STAGE3_CONTRACT.md:1257-1258` explicitly retain the launcher requirement after that repair. A sample or startup receipt from the mutation runner is not the canonical science process's independent launch attestation.

Minimum closure evidence:

1. Define the launcher and the measured code boundary separately, then run the actual canonical entrypoint through it.
2. Bind the resolved source bytes actually used for execution to a run/phase receipt, with a clear startup/import scope. A hash of a convenient pristine directory alone does not establish this.
3. Verify normal execution plus rejection or accurately reported failure for a different module/source selected at launch, and show the receipt is consumed by the relevant result validator.
4. Keep the assurance bounded to the existing deployment assumptions; no new universal resistance to an administrator rewriting both program and evidence is required by this review.

While open, say that runtime source attribution is self-measured and not independently launcher-attested. Do not call an earlier decoy-specific guard equivalent to this closure.

## E4: report verification is not scenario replay

`docs/22p_gap/mutation_replay.py:7106-7201`, `check_coverage`, checks registry/HEAD/tree/environment/preimage bindings, then reads report files and combines declared observations. `:6830-6881`, `verify_receipts`, hashes those report bytes, verifies report identity, and re-derives verdicts. `:6960-6984`, `_verdict_from_reports`, reads saved JSON before/after reports; its own comment at `:6967-6968` states the remaining fabricated-report limitation. None of those paths calls `_replay` to reproduce the scenarios.

The distinction is already explicit in `_execution_receipt` at `:6261-6263` and `GATE54_REQUEST.md:93-102`. It is not a newly discovered run defect. The `run.sh` grid/fit/score/report path does not call mutation replay or coverage checking, so an unverified report can overstate test assurance without being an input to the numerical solver.

Minimum closure evidence:

1. An independently initiated checker constructs the reviewed sandbox from fixed source and applies registered mutations itself.
2. For every scenario claimed replayed, preserve baseline and mutant call-phase outcomes for the expected node and witness, with code/environment identity; enforce the existing fail-closed and no-op/preimage requirements.
3. Record the selected population, deterministic seed/selection policy, completed scenarios and all unperformed/declared cases.
4. Sampling may support an explicitly sampled assurance claim. `GATE70_REQUEST.md:37` proposes sampling; that does not close an unqualified claim of independent replay for the whole coverage population. Either keep E4 partial/open or explicitly redefine its acceptance scope as sampled replay.

## Missing execution-plan condition found during this audit

The exact command in `GATE70_REQUEST.md:57` is `./run.sh`, with claimed output at `results/grid_fit_v4/` and an archive in the same execution.

- `run.sh:17` initializes empty MODE and `:213` exits 1 when `--mode` is absent.
- `run.sh:60` defaults the output to a timestamped `results/run_...` path, not `results/grid_fit_v4/`.
- Even `--mode all` is explicitly grid -> fit -> finalize -> score -> report (`:509-565`); it does not invoke the archive tool.
- The archive operations are in the separate `scripts/archive_results.sh:141-160` (bundle/check/restore-validation).

This is a concrete missing workflow specification, independent of E1/E2/E4. Before a conditional run, require the exact effective argv, output/config/protocol/leg identity and archive/receipt commands, together with matching planned authorization and a no-science preflight. Merely marking the E1-E8 table complete cannot make the literal requested command run. The root reviewer is independently checking the execution/lifecycle prerequisites; this subreview does not set their final severity or GO verdict.

## Suggested result-label content

The count-only wording at `GATE70_REQUEST.md:62` does not say what evidence supports each claim. Use named limitations and actual observed results instead, for example:

> Conditional run under the documented single-principal/local-filesystem scope. Local validators: [actual results and receipt identifiers]. E1 open: projection producer attribution is not independently verified. E2 open: runtime source attribution is self-measured, with no independent trusted-launcher attestation. E4 open: mutation coverage reports were checked for consistency; independent replay was [not performed / performed only for the listed sample]. E6: [registry-scope statement from that review]. No claim of fully independent provenance or full independent mutation replay.

The final reviewer should substitute real outcomes and the separately reviewed E3/E5/E6 status. These limitations do not certify the calculation's scientific external validity; that is outside this subtask.

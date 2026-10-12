# R7 contract/provenance review

Pin: `3cedd40a5911d0606bf33ed2085d5cb93c4db2e0`. Scope: request Q3, patch scope, independently anchored registration, and launch boundaries. Supplemental20 is excluded. No new blocking contract finding was found. Closure of G2RR6-01 still depends on the independent consumer/mutation checks performed by the other review lanes.

## Independent evidence

`probes/r7_contract.py` ran successfully using the supplied Python runtime (`-X utf8 -B`); output is `evidence/r7_contract.json`. It hashes source files, parses ASTs and raw contact data, and does not run production code, solvers, or case15 networks. An initial run encountered Windows' long-path limit on one evidence filename; the probe was corrected to use the extended-length path prefix and the entire check rerun successfully. No source files changed.

- All **573** review-copy files match both the supplied manifest SHA-256 and the pinned API tree Git blob SHA-1/size; no mismatches. The attached request is byte-identical to the request at the review pin.
- The **32 sealed files** are independently byte-identical to the previous R6 review copy. `code_fp = e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`, matching registration. `CODE_FILES` is at `scripts/run_network_194_parallel.py:183`; fingerprint serialization is at `:1211-1215`.
- All four case15 raw files independently match the full 64-character README hashes and uncompressed byte counts, including streamed gzip decompression for both dumps. This is independent review evidence; S0b itself checks 12-character prefixes and must not be described as rehashing the raw bytes.
- The raw contact gzip contains **182,995** rows. A direct parser using `decimal.Decimal`, separate from the producer/shared validator, found exactly the two negative contacts and independently applied the registered unit scales and six-decimal rounding: `[31,29241,-0.186036,1.05114]`, `[38,29241,-0.186264,1.0512]`. These equal `negative_rows_ref` at `scripts/g2_network_reread.py:125`.
- All **seven** imported `r6_s0b_*.input.json` files are byte-identical to the original independent R6 review files.

## Actual patch scope

Fix `ec9c5114936c9973e2bcff9d53715e01d021c321`, parent `821f0e15180bdd3472f9ce203a7a7815a1f27eb9`, changes precisely two source files. Both fix-commit blobs equal the corresponding blobs at the R7 review pin. The entire R6-to-R7 compare has the same two changed `scripts/` or `webapp/` files; its other changes are documentation/evidence and are not an expansion of this review into supplemental20.

- `g2_network_reread.py`: **161 insertions / 8 deletions**. Existing functions changed: `case15_negctl_verdicts`, `_selftest`. Four helpers added: `_c15_hexn`, `_c15_real`, `_c15_raw_sha_verdict`, `_c15_negative_rows`. The changes in `nc1` and `nc2` at `:350-362` implement the approved same-class tightening. Existing nc4/ionic limits and nc5/attempt validation are unchanged.
- `wsl_network_smoke.py`: **2 insertions / 0 deletions**, both at `:919-920` inside **`_c15_fixture`**: a comment and fixture `raw_sha` initialization. Every other top-level function's AST is identical. All **20** `chk(...)` AST calls are identical before/after. The actual raw-hashing producer `stage_refbed` at `:355-372` and actual contact reporting at `:204-218` are unchanged.
- Reread static `chk` calls rise from 24 to 27; this is not the runtime assertion count (one mutually exclusive branch). The request's runtime 23→26 count must be checked by executing its selftest, as the parent review lane does.

## Selftest independence and registration drift

The smoke fixture at `wsl_network_smoke.py:920` obtains its positive hash entries from `CASE15_NEGCTL`; that positive test alone would be circular. The overall regression has independent anchors:

1. Reread's positive fixture has independently hardcoded 12-character values (`g2_network_reread.py:1198-1200`) and explicit negative rows (`:1214`).
2. The seven preserved WSL/independent-review JSON inputs are consumed through actual `main(['--smoke-root',...])` at `:1366-1385`; they are not regenerated with the new expected constants.
3. The new selftest compares all four full registry digests to the committed README at `:1388-1394`.
4. This review independently checks actual raw bytes and negative rows as above. The unchanged producer derives raw hashes from files/README (`wsl_network_smoke.py:365-371`) and negative row display values from raw contact columns (`:204-218`), not from the new registration.

Consequently, there is no present registry drift. Exact negative-row equality is appropriate only for this fixed case15 artifact and its existing six-decimal report format; it must not be generalized into a tolerance for arbitrary scientific inputs. A future fixture or producer-format change needs a reviewed registration change and renewed positive evidence. README's experimental provenance caveat still applies: its bytes do not independently establish which original DEM run produced them (`docs/data/case15_corner_20261001/README.md:4-5`).

## Q3 and conditional GO boundary

If the consumer lane confirms G2RR6-01 closure, no new numerical campaign or sealed-code change is indicated by this review. Q3 is supportable as a **conditional return to the existing 194 launch workflow**, not a statement that a 194 launch or release has already been approved or passed.

- Author's distinct launch approval remains required (`lhs_network_batch_registration_20261007_g2.md:23-25`; R6 review §6-2). Approval to complete this review request is not that launch approval.
- Record the chosen launch commit and both handover-tool hashes. `HANDOVER_FILES` at `run_network_194_parallel.py:237` explicitly includes reread. Its SHA-256 changed from `71945dab069f87c4f48d425f5768374e5d0bd43ffb1e79467131a817959486dd` to **`248ee5c08bc57751405912454a543a5a5197e29c8869f344e9bd7af4300a63ad`**. `lhs_design_dataset.py` remains `27c9c1a8a680945c5ba60e6717e1d77438a489549a62eb24bddb65223c0a8b29`. The launcher records these at `:2385`; unchanged numerical `code_fp` does not imply unchanged handover tools.
- The fixed launch pin needs the registered tool precheck, including smoke **fast16 + real4**. The old WSL logs are evidence for their old tool bytes, not a substitute for running changed launch-pin tools. R6 §5 already accepts this distinction; R7 request §3 explicitly corrects it. `selftest_inventory.tsv:216-217` continues to distinguish fast from slow. R7 closure itself can be shown by rereading existing WSL records; it does not require another 194/pilot/case15 campaign.
- Use a clean tree and fresh ROOT, confirm the 32 hashes, expected g2 and input fingerprints, and enable `--observe-imports`. Launcher locations: `:1670-1701` (hash/dependency/generation/input checks), `:1685-1687` (observation requirement), `:1717` (dirty rejection), `:2332-2334` (nonempty ROOT rejection). The authoritative amended command is the observation-ON block; registration's preserved old commands are historical (`registration:328-333`).
- Completion is a later gate: exact registered 194 final IDs all SEALED, full completed-attempt set equals stage-binding set with per-attempt `expected=observed`, audit success, detailed `--expect-set production194` reread, then handover/release gates (`registration:224-244,248-254`). Retries can legitimately make completed-attempt counts exceed 194; do not replace the final-ID requirement with an attempt count.
- Preserve original command rc, dirty/version text, and before/after fingerprints in the next evidence package. The old package limitation was documented at `codex_gen2_network_reverify6_precheck_20261009/README.md:38-39`; it is not evidence of numerical invalidity or a reason to rerun the old campaign.
- This review provides no supplemental20 support assessment and no 214-case release GO.

No git operation, production edit, DEM/MPM simulation, run194, or costly `--selftest-real` was performed in this lane.

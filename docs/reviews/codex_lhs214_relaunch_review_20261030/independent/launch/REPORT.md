# Independent LHS214 relaunch review — launch protocol

Review pin: `bf8cf21c6466cdb9411f9320711b871c2d1c651e`.
Launch pin B7: `35f0327377a4213774010a090df4d224e50d29e1`.
Reviewed source root: `C:/Users/Administrator/Documents/Codex/lhs30/repo`.

## Decision

- **Q1(iii): closed under the explicitly accepted revised criterion.** B15's original “only documents/ledger changed” condition remains strictly unsatisfied. Do not mark that literal condition as satisfied. The author's recorded Q2(a) adopts the active ratified §3 criterion for this launch, and the available pinned source supports that reading.
- **Q2: procedural GO for the registered manual 194 → audit/check → supp20 sequence at B7, with full 40-character `--approved-sha`.** This is not an unconditional copy/paste script or a claim that each displayed warning aborts the shell. Author launch approval and the existing immediate pin/environment/ROOT checks remain prerequisites. The review does not authorize execution.
- **New actual blockers found in this assigned scope: none.** The known `L214P-02` remains open; the full40 launch-receipt mitigation is effective for the documented defect. No model, physics, production-completion, or deployment GO follows.

Q1(i), Q1(ii), and the complete Q1(iv) evidence audit belong to the parallel reviews. This report does not independently close those broader questions.

## Q1(iii): original B15 versus author-selected revision

The 194 registration at `docs/reviews/lhs_network_batch_registration_20261007_g2.md:125–127` retains the old restriction that the launch commit be the document commit or a subsequent commit changing only documents/ledger. The later active ratified definition at lines **182–188**, specifically **187**, defines B7 as one author-selected pushed main-branch SHA containing the ratified text whose 194 dry-run reports the active code fingerprint.

The execution sheet explicitly exposes the conflict, rather than hiding it: `docs/reviews/lhs214_relaunch_exec_sheet_20261027.md:86–91` says strict B15 fails because the runner fix follows the last registration commit. Its **223–226** records the author's “lhs 권고대로” adoption of Q2(a): use the active ratified line and disclose the strict failure. The request repeats the qualification at `docs/reviews/codex_lhs214_relaunch_check_request_20261028.md:98` and asks precisely that interpretation at **149**. Therefore this is an expressly selected exception/revised criterion, not proof that Python changes somehow count as documents.

Independent local code hashing yielded `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` over 32 source files. Runner SHA256 is `3220be53fb89cd16c81f0273c8b9f7444f262c5311d02b2017756fd94fd66ac8`; receipt SHA256 is `3d6110be24d24bf91ad1e71232a2e5dad580cf95178d6135b13aa6ca6de6f950`. These match the declared B7 artifacts. Historical commit ancestry and `.py 37` diff counts are supplied evidence in this source archive, not fresh local git measurements; no `.git` checkout was available or mutated here.

## Q2: what the exact final block does

`docs/reviews/lhs214_relaunch_package_20261020.md:376–385` is expressly labelled a form/outline after author approval, using the same shell variables and same pin. It invokes production194 at **380**, directs completion plus the 194 registration §4 checks at **382**, invokes supp20 with `--cohorts lhss` at **383**, and invokes the two-manifest launch receipt with `--approved-sha "$PIN"` at **384**. The request at **137–142** preserves these requirements. The execution sheet at **132** says to paste and inspect each stage, not join them into one script, and at **219** places author approval after the review.

The manual completion check at line 382 is substantive. The 194 registration **229–231** requires audit output, and **257–274** replaces naive attempt counts with retry-aware expectations: final case set 194, all required seals, completed-attempt keys equal stage-binding keys, per-attempt expected=observed, no observation problems, and reporting unfinished noncompleted attempts. It must target the actual `$R194` ROOT; the older registration examples spell their local ROOT variable `$R`.

The source does not implement a cross-batch gate: `cmd_run` (`scripts/run_network_194_parallel.py:2617–2700`) has no approved-SHA argument and the supp20 call does not consult the 194 outcome. The command parser at **3138–3164** confirms this. Its preflight rejects dirty tracked files at **1767–1771** and nonempty ROOTs at **2623–2626**, but those facts do not replace the documented final pin/environment/ROOT check. It accepts an already-existing empty directory, so the stronger “previously nonexistent name” condition remains manual. The receipt's H1 at `scripts/supp20_input_receipt.py:484–489` checks different resolved manifest folders, matching SHA, and matching seal fingerprint; it does not prove historical nonexistence.

The setup pin comparison at execution-sheet **140** prints a stop message on mismatch; it is not `exit`/`return`. Dirty and existing-name lines **141** and **146** similarly report conditions. The production pipelines at package **380** and **383** have `tee | tail` and no `PIPESTATUS[0]` check or conditional chaining. A failed run is not an automatic shell stop. These are **source-only shell observations**; Bash/WSL was not executed or emulated.

A source-level counterexample is a failed/nonzero 194 runner followed by successful `tail`, after which a blindly pasted block reaches the independent supp20 command. Another is a mismatched clean HEAD after the earlier preflight: `run` has no approval input, so approval mismatch is caught only by the later receipt. Both require skipping the explicitly registered manual stop/pin/check conditions. They therefore limit what can be certified about automation; they are not new blockers against the specified manual procedure. Do not describe the outline as fail-fast or approve whole-block unattended execution.

## L214P-02 mitigation: independent dynamic evidence

Reproduction (Windows PowerShell; pure validators only):

```powershell
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -I -X utf8 -B 'C:\Users\Administrator\Documents\Codex\lhs30\independent\launch\check_launch_validators.py'
```

Artifacts: `check_launch_validators.py`, ten synthetic manifest fixtures, and `validator_results.json` in this directory. Runtime: Python 3.12.14. The actual imported `launch_eligibility` and `_manifest_checks` functions were called with synthetic JSON; no launch, retry, audit CLI, selftest, solver, WSL, shell, or git subprocess was called.

| Manifest SHA | Approved argument | `launch_eligibility` | F7 result |
|---|---|---|---|
| Exact B7, 40 characters | Exact B7, 40 characters | current | true |
| Exact B7 plus LF | Exact B7, 40 characters | current | false |
| Exact B7 plus LF | B7 first 7 characters | current | false |
| Exact B7 plus LF | absent | current | check absent |
| Valid 40 characters, last digit changed to `0` | Exact B7, 40 characters | current | false |
| Same wrong 40-character SHA | B7 first 7 characters | current | true |
| Same wrong SHA | absent or empty string | current | check absent |
| Missing SHA or only 7 characters | Exact B7, 40 characters | invalid | false |

These reproduce the relevant boundaries exactly. The remaining defect is `_HEX40.match(g['sha'])` at `scripts/run_network_194_parallel.py:1140`, with `$` accepting a final LF. `_manifest_checks` at `scripts/supp20_input_receipt.py:357–361` uses `re.fullmatch(r'[0-9a-f]{40}', g['sha'])` and `startswith(a)`. A full 40-character approval makes that prefix check exact equality. F7 and G7 use this same function, only the label/set differs. Missing or empty approval omits the checks by the `if approved_sha` branch, and `receipt` at **479–481** records a warning rather than a failure.

Important distinction: **short7 still rejects the malformed LF SHA** because the manifest must independently fullmatch 40 characters; short7's weakness is accepting a different valid 40-character SHA sharing the prefix. The documented full40 argument closes both paths for this invocation. The request's deferred fix policy does not claim that `launch_eligibility` itself is fixed.

The source archive omits harvest data. Consequently the synthetic `_manifest_checks` runs correctly report F2 false for missing registered-set enumeration. The table reports the actual focused F1/F7 results, **not** a manufactured full-receipt rc=0. The complete receipt's aggregation at **491** requires all checks true; F7/G7 false therefore prevents rc=0 in any otherwise-passing launch receipt.

## Current state and retry limits

Three further synthetic manifests remained `current` when (a) completion fields were absent, (b) `status='running', completed=False`, or (c) a retry record declared dirty/mixed overrides. This matches `launch_eligibility`'s documented purpose at **1093–1100**: execution format eligibility, not production completion or retry-policy approval. The launch receipt uses that limited meaning at **338–339** and does not audit worker results.

The actual retry command still applies additional gates: **2907–2929** reject noncurrent format or changed seal/generation/dirty state unless explicitly permitted; **2953–2959** record override flags. `retry_todo` at **2875–2900** skips live workers, keeps already sealed done/partial records, and selects missing/failed/unsealed records. The registration's retry-aware manual audit expectations are therefore necessary and are already included by package line 382. No requirement to force every attempt count back to 194 was inferred, and `current` was not promoted to completion.

No protected source was edited. All newly written files are in `C:/Users/Administrator/Documents/Codex/lhs30/independent/launch/`.

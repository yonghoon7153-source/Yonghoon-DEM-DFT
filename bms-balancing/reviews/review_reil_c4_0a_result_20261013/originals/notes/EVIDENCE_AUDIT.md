# C4-0a evidence and authorization audit

Frozen repository: `yonghoon7153-source/Yonghoon-DEM-DFT@c542e056b33d25100bc0519ce492c98d3bcce172`.
Audit scope: read-only source/log/JSON inspection, independent JSON arithmetic, source hashing, and byte comparison of the generated synthetic Sobol seals. No supplied program, import, test, optimizer, COMSOL, scientific xlsx/pkl, or notebook was executed/opened. Source paths below are relative to `bms-balancing/`.

## Conclusion

The submitted five recorded command outcomes, source identities, four generated Phase A array payloads, and 66-call dry-run arithmetic are supported. This is evidence acceptance for what was actually recorded, not proof that the implementation has no defects or that actual E3a/H work is authorized. Other code-review findings may block acceptance of the implementation.

The user-authorized C4-0 split and executor-selected array deferral are separate events. The split permits one RED and one GREEN suite per substage; it does not authorize moving three array groups out of C4-0a. The deferral is technically compatible with the requirement to finish sealing before the first C4 local execution, provided the rules remain fixed, all 16 simultaneous starts are sealed and only the first 12 used, and the new scope is ratified before C4-0b. Do not describe the original C4-0a scope as fully completed or the deferral as previously approved.

## Approval and scope coordinates

- `docs/REIL_PREREQUISITES_STATUS_20261004.md:673-684`: received limited acceptance of the new environment seal; accepted C6 check credited once; explicit full manifest argument required.
- Same file `728-744`: user selected the split; each substage gets 4 hours, RED 1/GREEN 1, compute at most 1,800 s. This explains the total of two RED/two GREEN suites and is not an unauthorized retry.
- Same file `733`: original C4-0a includes A1/A2 Phase A, profile Sobol 2, simultaneous Sobol 16, and label-seed arrays.
- Same file `772-775`: executor admits moving the latter three groups during execution without user confirmation. `reil_c4_arrays_20261013/ARRAYS.json:92-100` records the omission; `scripts/reil_c4_e3a.py:56-61` fixes the same scope in source.
- `docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md:152-156`: seal before the first C4 local execution; all 16 simultaneous points sealed, first 12 used. The planned deferral does not itself establish an actual missed scientific-execution deadline: none is recorded here.
- Status file `802-810`: subsequent user selection is to wait for the C4-0a review. Line 810 explicitly preserves the requirement for user confirmation before C4-0b. A favorable review alone is not that confirmation.
- Status file `784-787` discloses three static corrections before GREEN. The no-fix/retest rule in approval request `179-180` is triggered by unexpected GREEN failure or unrelated RED harness failure, neither of which appears in the saved logs. The static corrections are not evidence of extra test runs.

## Recorded runs and time limits

Five `*.meta.json` records use the same start/end HEAD `3fabeb70e83931bfd8b46d6bde267b2b0e832ea1` and have `timed_out=false`.

| Step | Timeout seconds | Recorded elapsed seconds | rc |
|---|---:|---:|---:|
| Identity | 60 | 17.496 | 0 |
| RED | 600 | 4.386 | 1 |
| GREEN | 600 | 12.769 | 0 |
| Seal arrays | 240 | 2.523 | 0 |
| Dry run | 300 | 1.168 | 0 |

Independent sum: 38.342 s, matching `06_end.json:4`; allocated timeouts sum to 1,800 s. These are subprocess intervals from `00_step_runner.py:48-54`, not the complete authoring/commit duration. The start record predates the identity run, so authoring time is not silently put inside the compute sum.

`06_end.json:6,60-64` expressly labels 2,074 s as elapsed time at that record and excludes later commit/push/documentation work. Keep this as a pre-commit snapshot. The saved evidence does not independently establish the final complete-work endpoint or a continuous resource peak. The seconds-truncated UTC fields differ by 2,073 s, while the recorded elapsed value is 2,074 s; no material limit violation is implied by this one-second display difference.

RED raw stdout has 26 failure entries, all `NotImplementedError: C4-0a RED — 구현 전`, ending with `26 failed in 3.60s`. This proves failure against the stubs, not that every assertion would independently discriminate every possible broken implementation. GREEN raw stdout is exactly the pytest summary `26 passed in 12.16s` and the progress line. All five stderr files are empty; the original GitHub GREEN stderr blob is `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`.

The RED/GREEN test SHA is the same. All seven GREEN source SHA values were independently checked against current original bytes and match the end record. `tests/conftest.py`, C5, C6, and P0 additionally have identical Git blob IDs at the start commit and frozen review HEAD. This supports no change to those four inherited files. A source-hash list does not by itself prove absence of all unlogged executions, so 'no auto-fix/retest' remains bounded by the supplied execution record.

## Hash and environment bindings

Verified source SHA256 values:

| File | SHA256 |
|---|---|
| `tests/test_reil_c4_0a.py` | `6b2635d4a97e296a4d2d8749209b66461d3bbfd9009465aaeac3d80a57197e17` |
| `scripts/reil_c4_monitor.py` | `0c6ed54ff79422ad2a3d3964a0f743a0b5616da2c21138ddad8ddd85a9c6e892` |
| `scripts/reil_c4_e3a.py` | `14751a75e14728bb1ddfc8656d736b84b9298d399f932a0c56a35987b3045bb0` |
| `tests/conftest.py` | `6ecf97fbdeeb4919bb467a88558d09bfc9c7d4c317816e5c92a693858f360bc7` |
| `scripts/reil_c5_pilot.py` | `73bee8dc412b39863afb64b70bc128cbecee2075a3a17914fc7288f353ef11a6` |
| `scripts/reil_c6_profile.py` | `408afc4bb5eb1069583b955e0eb6215bf48dd9259ad474c230549d1b3642df5d` |
| `scripts/reil_p0.py` | `793b326ebf86a6db3b855d828aff4d6b6dddc824bed8d00f4161537b1cc06e3a` |

The identity, array-seal command, and dry-run command explicitly pass the accepted C6 directory and complete manifest SHA `4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc`. `01_identity.json` records `ok=true`, `problems=[]`, current lock `ea91156c…1faa`, and profile `50f2c7fb…a641`. The static implementation (`reil_c5_pilot.py:658-701`; `reil_c4_e3a.py:410-424`) checks manifest members, lock, profile, options, and implementation hashes without invoking full C6 check. This is the intended credited-check identity check, not a newly demonstrated full functional check.

The metadata records the same 15 removed environment variable names, thread limits, scratch paths, and pytest path. This is limited child-environment hygiene; the filtering is not a proof of complete environment isolation or a full independent secret scan. The 46/46 submitted blob-check and zero-secret claims have no separately saved audit report in the inspected command evidence; avoid silently turning them into independent observations by this subreview.

## Phase A seal verification

C4 manifest SHA independently equals `861c33aceb40befd3f707f2aa0b53fe159031f75766e91fff765666254d8b06c`. ARRAYS metadata reports four little-endian float64 arrays of shape `(64,4)`, and no generation warnings. Independent base64 retrieval of each generated C4 `.npy` and the corresponding accepted C6 `.npy` found exact byte equality for all four. Each file has 2,176 bytes and NPY v1 header `descr='<f8', fortran_order=False, shape=(64,4)`; raw payload length is 2,048 bytes. Both full-file SHA and raw-payload SHA match C4 metadata and C6 `SOBOL_PHASE_A.json`:

| Array | NPY SHA prefix | Raw SHA prefix | C4/C6 Git blob ID |
|---|---|---|---|
| A0 seed 0 | `916ac3733713` | `6b9d62ada1cf` | `3af0eb0d59dca49ad310ea1043d255076bb56a4c` |
| A0 seed 1 | `0e8daccaf054` | `569ecedbb240` | `5d26643d385a3eb9cbee7539000143e089a7e874` |
| A1/A2 seed 0 | `2e7ba141ddf0` | `597d508bfd674` | `c2fe477561e5a2dd0de383863bfcbc3d290c699f` |
| A1/A2 seed 1 | `72a3372631a5` | `8f45db97c6ef` | `5895f7dfe0a8adc14cd08e8b1ad20492d65665b9` |

This independently accepts the current four payloads even if the general `check_arrays` verifier has a separate fail-open weakness. It does not close the three deferred array groups.

## Dry-run arithmetic and limits

`05_dryrun/PLAN.json` SHA independently equals `8f034bf4dd0d797edaf930ffb1119a9dfb9815ad6789db74d1975250dacdb64a`. Independent parsing of the complete 66-call list confirms unique IDs 0–65, `call_id=case*11+row`, worker=`call_id%4`, all six case selections, all 11 extraction rows with matching row and `status=OK`, and the stated populations/generations/seeds.

- GA: 11 calls × 20 runs × 50 population × 100 generations = 1,100,000 expected evaluations.
- NSGA2: 44 calls × 1 run × 50 × 100 = 220,000.
- NSGA3: 11 calls × 1 run × 165 × 100 = 181,500.
- Total: 66 calls, 275 optimizer runs, 1,501,500 arithmetic expected evaluations.
- Worker totals: 404,500 / 404,500 / 388,000 / 304,500, matching PLAN lines 2534–2540.

These are arithmetic expectations, not measured execution counts or hard caps. PLAN `2569-2580` and the static dry-run body `reil_c4_e3a.py:444-503` agree on optimizer calls 0, objective calls 0, util import false. The body hashes/parses util source, verifies the excerpt case table, checks identity and arrays, and reads prior P0 JSON; it does not call the optimizer.

## Nonblocking evidence limitation: preserve an unambiguous synthetic outcome

Exact coordinates: `tests/test_reil_c4_0a.py:349-363`, especially `357-362`; `docs/REIL_PREREQUISITES_STATUS_20261004.md:788-789`; `03_green.stdout.log:1-2`.

The preserved-util NSGA2 test passes after either a returned result or a local util error, and pytest captures its printed outcome. Therefore the current GREEN record establishes that this contract test passed, but does not establish a successful end-to-end NSGA2 return or how many objective calls it performed. The submitter already discloses this limitation. Preserve the current run as-is; an additional execution would consume new authorization. For the next authorized suite, persist its returned/error branch, count, and exception summary as ordinary evidence even on passing tests. Do not describe the current record as 'real util optimization completed successfully.'

## Capture handling

Initial reviewer-side text captures had one extra terminal LF from capture creation. That was identified as a capture artifact, not a repository discrepancy. The parent restored original structured-content bytes and created `SOURCE_INDEX.json`; the hashes above were checked after restoration or directly against original GitHub content. No production source was modified by this subreview.

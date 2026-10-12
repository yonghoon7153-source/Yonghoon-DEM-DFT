# R7 independent predicate review — Q1 / Q2

Pin: `3cedd40a5911d0606bf33ed2085d5cb93c4db2e0`. Source was read only. No git commands, WSL runs, DEM runs, or network solves were executed by this reviewer. The probe imports only the predicate module and smoke module, calls the pure predicate/evaluator functions, and reads the fixed compressed contact dump to check its display conversion.

## Result

No additional blocking finding in the changed predicate contract. Q1's raw-hash detail and negative-area detail repairs hold under independent adversarial inputs. Q2's strict registration, row shape/value, single failure-stage, and flat tau-number checks accept the actual 10-09 record and compatible representation changes. The parent reviewer owns CLI integration and the real positive pipeline; this note does not claim to replace those checks.

`probes/r7_predicates.py` completed with rc 0 and emitted `evidence/r7_predicates.json`: 232 cases, zero unexpected outcomes, zero producer/shared-predicate disagreements.

| Group | Cases | Outcome |
|---|---:|---|
| Actual positive and compatible metamorphs | 12 | Accept |
| SHA detail mutants | 88 | Reject |
| Negative-row mutants | 82 | Reject |
| Alternate formats the current producer does not emit | 3 | Reject |
| Failure-stage/publication mutants | 11 | Reject |
| Tau/status mutants | 31 | Reject |
| Out-of-schema unknown tau fields | 5 | Accept; bounded observation below |

## Evidence and contract reasoning

1. `source/scripts/g2_network_reread.py:174`–`:196` validates the four-key raw map, pair length, lowercase 12-character hexadecimal type/shape, pair equality, registered prefix equality, and strict Boolean summary flag. Each registered file and each pair side was independently changed: wrong hash, uppercase, full 64-character hash, short hash, nonhex string, integer, bool, and null. Matching-but-wrong pairs, missing/extra keys, wrong pair lengths, invalid containers, and false-like summary flags are rejected. Key ordering and producer tuple pairs pass. The registration matches the README table. This is prefix-detail validation, not rehashing full source bytes, consistent with the accepted scope.

2. `source/scripts/g2_network_reread.py:199`–`:224` enforces two complete rows, strict integer IDs, finite non-Boolean real area/delta, signs, uniqueness, and equality to the registered display values. The producer reads IDs directly from `c_cpl[7]` / `c_cpl[8]` in `source/scripts/wsl_network_smoke.py:204`–`:205` and emits a list with unit conversion plus `round(..., 6)` at `:217`–`:218`. Direct read of the fixed gzip yields exactly `(31, 29241, -0.186036, 1.05114)` and `(38, 29241, -0.186264, 1.0512)` after that conversion. The first raw delta conversion is `1.0511400000000002`; it becomes `1.05114` in the producer. Therefore rejection of the unrounded value, a one-ULP change, or an extra-decimal value is not overblocking the current producer.

3. Row order reversal passes. Decimal/scientific JSON spellings with the same numerical values pass. Swapping contact endpoints or moving one pair's area/delta to the other pair is rejected. Endpoint swapping is physically compatible with an undirected edge, but it is not an alternate output of this fixed report producer: the registered raw bytes fix the ordered fields. The top-level tuple-row container is also outside the current list-comprehension/JSON producer contract; inner tuples are explicitly supported and pass.

4. `source/scripts/g2_network_reread.py:349`–`:354` rejects duplicate, missing, or extra reported failure stages. This is compatible with `source/webapp/pipeline_service.py:1759`–`:1768`: when any required stage fails, `summarize` returns the required failures, not the optional failures. Thus an optional coverage failure does not by itself add another reported failure stage alongside the required solver failure. No positive-path conflict was identified with the exact singleton requirement.

5. `source/scripts/g2_network_reread.py:356`–`:362` rejects every tested top-level integer/float tau value, including zero/NaN/Inf and keys outside the three numeric prefixes. Registered numeric prefixes also reject bool, numeric strings, and nested containers. All three required statuses remain checked. Removing null numeric fields or replacing null with empty-string blank cells passes.

6. `source/scripts/wsl_network_smoke.py:683`–`:688` routes producer checks to the same shared predicate; the probe verifies agreement for every tested report. `source/scripts/g2_network_reread.py:406`–`:419` uses stable IDs and fresh predicates, so check-list order is immaterial. Exchanging two display names' IDs while retaining the complete all-PASS ID set also passes, but it does not hide a report defect: report predicates are independently recomputed by ID. Display text is not a separate evidence authority.

## Bounded observation, not a new blocker

Adding `tau.extra = {"tau_ion_hertz": 1.5}`, `[1.5]`, a deeper nested dictionary, a numeric string, or a bool is accepted. The new numeric scan is shallow and excludes bool (`source/scripts/g2_network_reread.py:360`–`:361`); it is not a recursive validator for arbitrary JSON. These are recorded as five observed accepts, not silently omitted from the probe.

The current producer filters a flat `case_row` mapping in `source/scripts/wsl_network_smoke.py:351`; `source/scripts/tau_flux.py:1148`–`:1156` constructs that row from named scalar columns. Unknown nested extension fields are not current producer output, and a nested value under an existing numeric prefix is rejected. Accordingly this is neither a demonstrated normal-path regression nor a reason to keep G2RR6-01 open. Wording such as “tau 칸 어디든” should be read as every top-level cell in the current flat tau schema; if future versions add nested values, recursive validation or an explicit flat-shape check would be needed then.

## Reproduction

From the review directory:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B probes/r7_predicates.py
```

The JSON stores source/evidence SHA256 fingerprints, the independently read raw rows, each named mutation's expectation and actual verdict, S0b problem count, and producer/shared agreement. It emits JSON on stdout and does not write under source.

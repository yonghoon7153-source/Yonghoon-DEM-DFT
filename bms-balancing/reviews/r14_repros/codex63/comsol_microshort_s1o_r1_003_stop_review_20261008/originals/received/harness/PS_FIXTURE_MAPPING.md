# PowerShell 31-case fixture mapping — R1_002, authored, NOT EXECUTED

Read `VALIDATION_PLAN_CORRECTED.json`, `PS_INPUT_RECIPES.json`, immutable Parent source and actual Python producer JSON. No handwritten Result summaries are used. Before loading any production function, `results/PS_PRODUCER_SEAL.json` must state Python99 PASS, match the immutable source manifest and current PS harness bytes, and bind the exact set of ten producer/context files. Each subsequent producer read again checks its exact bytes/SHA. Mutants are generated from these exact bytes in memory. The recipes and harness seal every mutation leaf and value. Expected result field/reason and function reach come from the corrected plan; each named case is one target invocation, no hidden positive-control invocation.

Actual producer mapping:

| Cases | Python producer | Mutation |
|---|---|---|
| PARENT01 | CHARGE01 | None, normal positive control; cache actual S1Decision return |
| PARENT02 | POLICY03 | None, exact exceedance accepted as valid comparison evidence |
| PARENT03 | CHARGE_R109 | None, protective 90/90.1 pair, safe prefix 249 independently bound to fixed 255 vector |
| PARENT04 | CHARGE01 | Native.rc integer0 to string0 |
| PARENT05 | CHARGE01 | Native.fatal false to true |
| PARENT06 | CHARGE01 | Remove Result.comparison_details |
| PARENT07 | CHARGE01 | Result.comparison to EXCEEDS_LIMITS only |
| PARENT08 | CHARGE01 | Result.effective_coefficients.grade to CONFIG_ONLY |
| PARENT09 | cached actual PARENT01 decision | Writer inert adapter throws INERT_WRITER_FAILURE; shared positive PARENT12 |
| PARENT10 | cached actual PARENT01 decision | Clock99,100.1; overall100; delivery20 starting90; total-only overrun; positive PARENT12 |
| PARENT11 | cached actual PARENT01 decision | Clock99,100.1; overall200; delivery10 starting90; delivery-only overrun; positive PARENT12 |
| PARENT12 | cached actual PARENT01 decision | Clock99,100; overall100; delivery10 starting90, successful inert writer/readback; inspect limited |
| PARENT13 | CHARGE01 | Remove Expected.end_s |
| PARENT14 | CHARGE03 | None, registered analyze result with charge INCONCLUSIVE; must remain valid but incomplete |
| PARENT15 | CHARGE01 | Remove Result.initial_profile |
| PARENT16 | cached actual PARENT01 decision | Clock99,100; deliveryStart100/overall100, no writer call; positive PARENT12 |
| PARENT_R101 | CHARGE01 | comparison_times[2]=comparison_times[1] |
| PARENT_R102 | CHARGE01 | comparison_times[2]=string0.00025; between original indices1 and3, nonrequest |
| PARENT_R103 | CHARGE01 | comparison_times[2]=stringNaN |
| PARENT_R104 | CHARGE01 | comparison_times[-1]=string120.1 |
| PARENT_R105 | CHARGE_R109 | comparison_times[-1]=string90.1, above safe90 |
| PARENT_R106 | CHARGE01 | Swap comparison_times[1] and[2] |
| PARENT_R107 | CHARGE01 | Replace full_intersection[1] string0.0001 with native-only string0.00015. Check neighbors0/0.0002 and native membership before mutation. Other native-only times may exist. Preserve order/count/endpoints; comparison list unchanged |
| PARENT_R108 | CHARGE_R109 | common_requested_count/comparison_count=255; comparison_times=full Expected vector; safe prefix still249 |
| PARENT_R109 | CHARGE01 | charge_budget.grid_binding.actual_end_s=string119.9 |
| PARENT_R110 | CHARGE01 | charge_budget.records[1].t_s=string0.000000015 |
| PARENT_R111 | CHARGE01 | charge_budget.grid_binding.global_identity.sha256=f repeated64 |
| PARENT_R112 | CHARGE01 | Remove charge_budget.grid_binding |
| PARENT_R113 | POLICY02 | In actual producer raw JSON, remove only the two quotes around the unique voltage_V.value token0.001; ConvertFrom-Json then must yield CLR Double before parent. Record mutant bytes/SHA and token offset; positive R115 |
| PARENT_R114 | POLICY03 | Only comparison and comparison_details.status to WITHIN_LIMITS_THIS_WINDOW; exact above-limit decimal unchanged; positive PARENT02 |
| PARENT_R115 | POLICY02 | None, exact inclusive0.001 lexical boundary |

All 15 source functions are extracted from corrected sealed line ranges, CRLF→LF only, trailing LF excluded; each SHA checked at session start. `S1Sha` is exactly line23/90bytes, SHA13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed. Terminal inactive throw is not loaded. No parent entrypoint exists or is invoked.

Command breakpoints observe actual S1Decision/S1NativeAxis/S1Fields/S1Coverage/S1ChargeFields/S1ComparisonNumerics/S1FinalReturn calls without changing the source bodies. Arithmetic helper breakpoints are not installed. Every result records reached names, target equality and expected reason/status; arbitrary exceptions are session FAIL. All writer/readback/clock adapters are in-memory only. No process, gate, Job, registry, native call or policy fallback is used.

PowerShell session must start only after Python99 PASS, producer JSON byte seals and source/harness/engine preseal. Runtime budget is one PS5.1 session, 300s. First unexpected failure stops remaining cases, writes first-error record and returns1, without retry or correction. This document makes no functional PASS claim.

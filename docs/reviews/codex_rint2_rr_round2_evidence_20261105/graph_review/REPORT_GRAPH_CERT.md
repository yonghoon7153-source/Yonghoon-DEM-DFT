# Rint ② RR round 2 — graph / certificate / source binding review

Review pin: `6917c3c9fa397936d3381ba1c1785562c5232e46`, branch `claude/stoic-knuth-NObVQ`.
Comparison baseline: `9bec6b7646374daed0d3edbb9647f9f46d302750`.
Date: 2026-11-05. Scope: bundle B/B″, RR1-01/02, RCA2-02/03/04, X6/X3/X5, RINT-23, Q3.

**Conclusion: the owned original minimum fixes close within the explicitly declared trusted-record boundary. No new actionable residual defect established in this subreview.** Q3 is demonstrably a remaining forgery boundary; it is not a claim of numerical proof verification by the consumer. Full Linux shell/ledger integration and real-machine compatibility were not rerun here.

All numerical tests used Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3, CPU, one numerical thread, `-B`. This is an independent local review environment, not the kgy 3.8 environment. The parent verified the supplied pin blobs and fetched omitted dependencies at the same pin. Principal producer and contract checks below were rerun after byte-exact dependency correction. No reviewed source was edited. All generated fixtures/evidence are under this review output.

## Finding-by-finding status

| Item | Status | Minimum fix and verified implementation | Independent evidence / remaining limit |
|---|---|---|---|
| RR1-01 P2 | **Closed for original counterexample and stated minimum fix** | `carbon_junction.py:2318` fingerprints retained DOF identities, exact parallel conductance sums and each electrode's conductances. `_assemble` attaches the fingerprint at `2612–2615`; `step3_sigma.py:2301–2308` reassembles main/lower/upper without solving. `ca_ext_svcf.py:537–551` checks the external expected fingerprints, including deleted upper endpoints. `rint_r_chain.py:2285–2287` rejects mismatch; final assessment at `6432` requires verified graphs. | Independently regenerated original parallel-edge k=0 circuit. Exact rational elimination gives ratio **1.0170715052190031**, inside the real certificate. Same-run main→lower certificate swap is rejected; original cut counts unchanged. Without source, assessment is `SV_UNCHECKED`. No demand for `G_cut != G_full`, so equipotential edges remain legitimate. Q3 below remains declared. |
| RCA2-04 reopened | **Closed to its remaining RR1-01 condition** | Retains version/kind/rule/current/input binding and topology checks at `ca_ext_svcf.py:608–662`; weighted-graph external binding closes the missing identity condition. `rint_r_chain.py:2268–2273` also compares the SV numerator certificate to the arm's actual main certificate including graph fingerprint. | Real contract accepts honest record and rejects original swap. Resident QD2–QD7/QG cover absent/foreign certificates, zero topology, cut relations and honest FLOAT cases. This does not claim re-proving arbitrary edited certificate numbers. |
| RR1-02 P3 | **Closed** | `step3_conv_cert.py:510–515`: KCL balance and absolute sum run under explicit over/invalid suppression; any nonfinite sum/balance returns an invalid target ledger. | Independently reran 3-node `gb=8e307`, `gt=1`, `phi=.2` under warnings=always and warnings=error. Zero warnings, no exception, `target_kcl_raw=None`, invalid ledger; `certify` returns `NOT_CERTIFIABLE`, `ok=False`. T25 **4/4**. |
| RCA2-02 P2 | **Closed for same-code minimum fixes, bounded execution evidence** | `rint_r_chain.py:891–925` checks Git command success and 40-hex HEAD; unknown dirty is rejected. `1889–1917` compares chain/runner HEAD and code bytes within a stage, exact runner bytes and environment presence; `1846–1857` includes environment unit and relative paths in the cross-stage key. `1707–1731` binds the registered R-plan blob to its declared commit. | Real generated Git fixture: clean accepted; outside-Git, unknown dirty status, short HEAD, untracked helper, and same-HEAD altered runner-folder certificate source rejected. NumPy-version change alters the code key. Static review confirms same-code gate call sites. No full shell-stage execution in this subreview, and no host attestation or protection against coordinated ledger/source falsification claimed. |
| RCA2-03 P2 | **Closed for same-bed minimum fix, bounded execution evidence** | `ca_s0_census.py:1082–1153` discovers canonical roles and hashes original bytes/settings. `rint_r_chain.py:1521–1536` deliberately excludes paths while comparing role SHA/size, metrics and settings; `1658–1668` rehashes and rejects mismatched kits. S0→arm off-grid comparison is at `2241–2242`. | Production discovery/hash/compare functions with small generated files accept honest kit and path-only copy; reject changed fibre, kind, settings and metrics with `S0_REPORT_MISMATCH`. For this Windows-only probe argv and settings extraction are explicit adapters; Linux bash expansion itself was not exercised. No real SBE/DBE kit read or solve. |
| X6 P2 | **Closed for original joint census-edit / upper-delete attack** | `rint_r_chain.py:1591–1624` seeds sealed census for same-convention DBE arm 0; `1627–1641`, `2277–2281` compare evidence and SV copies to that source. Separately `ca_ext_svcf.py:549–551` rejects a deleted upper when rebuilt source has one. | Independent real QDX and QD4: set unsplit counts in both internal copies to zero, delete upper, recompute aliases/interval. Internal contract accepts as before; both external census and graph source reject. This cleanly distinguishes record consistency from external binding. |
| X3 P3 | **Closed for original endpoint swap with unmodified counts** | `ca_ext_svcf.py:744–766`, `813–819` require typed lower-relative removal count and the upper↔lower topology relation; graph source also independently binds the endpoints. | Resident QX35 reproduces lower←upper rejection. Independent QDX/QD4 count mutations reject, including `n_reach_pairs_cut_vs_lower=None`, bool, float, string, negative, oversized integer and NaN. Coordinately replacing all numbers and expected graph claims is Q3, not a reopened X3. |
| X5 P3 | **Closed for original type/relation gap at non-computed endpoints** | `_topo_problem` checks count type/ranges and relations before the computed-endpoint-only branch (`ca_ext_svcf.py:722–770`). Thus +infinity endpoints no longer bypass those checks. | QX35 resident checks and independent real QD4 upper-zero fixture reject the adjacent malformed types/counts. Independent total **56** malformed count edits across QDX/QD4 all rejected. |
| RINT-23 P3 | **Closed** | `carbon_junction.py:403–449` serializes object-array contents with type tags and lengths instead of addresses; undefined content types rejected. Object grids rejected at `455–459` and `ptfe_face_alpha.py:83–88`. | Resident FP **19/19**, including fresh-object equivalence, changed-content rejection and separate isolated Python processes with heap preallocations 0/20,000. No pointer-byte identity dependence reproduced. |

The source-binding probe's phrase “unknown dirty” means `dirty=None`; its actual test name in JSON is `dirty_unknown`. Git safety configuration was passed only through the test process environment for its generated temporary repository. No global Git configuration changed.

## Independent reproductions and attack results

`probe_actual_binding.py` regenerates a small real raster→registry→plan→solve→certificate, produces a real manifest with producer helpers, and calls the actual `run_contract.ca_ext_record_ok`. A second raster/registry/plan rebuild runs graph-only with the solver replaced by an assertion that raises on any attempted solve. No solve occurred in that rebuild. The original circuit has 23 retained DOFs, unchanged cut counts and distinct main/lower fingerprints despite equal topology counts. Captured assembled matrices are in `actual_assemblies.json`; the exact Fraction elimination is implemented in the probe, independently of CG and certification.

| Case at illustrative threshold 1.01 | Contract with source | Graph state | Assessment |
|---|---|---|---|
| Honest real result | accept | verified | `SV_DEPENDENT` |
| Original main→lower certificate copy, G/ratio/aliases adjusted, counts unchanged | reject | mismatch | Consumer would stop `CA_EXT_RECORD`; direct assessment alone is conservatively `SV_UNCHECKED` |
| Honest result without graph source | internal-only accept | unverified / no_source | `SV_UNCHECKED` |
| Same swap plus lower certificate's `fp_cjunc_graph` changed to the rebuilt lower value | accept | verified | clear (`[]`) |

The final row reproduces the **already disclosed Q3 boundary** at registration line 736. It is not reported as a new finding. Honest interval is `[1.0170715052189403, 1.0170715052190658]`; the forged interval is `[0.9999999999999384, 1.0000000000000617]`. The fingerprint comparison authenticates which graph is *claimed* by the certificate and detects accidental/partial transplants; it does not establish that the certificate numbers were derived from that graph. The test threshold 1.01 is illustrative; the pin has no registered numeric production SV threshold and this is not a real-bed misclassification claim.

`probe_graph_core.py` additionally compares `_gfp_sums` against an independent `Fraction` oracle: **307** adversarial/random cases × three permutations = **921** exact comparisons, no mismatches. Cases include subnormals, cancellation, binary64 overflow in the exact sum, and both sides of the 512-term fast-path boundary. Exact equivalent decomposition/direction leaves fingerprint unchanged; adding a positive 2^-60 parallel term changes it even when rounded binary64 addition would not.

## Q3 recommendation

**Accept the current graph-bound SV inputs within the explicitly chosen trusted-producer/trusted-record operating boundary.** The original RR1-01 minimum fix does not require storing every phi or consumer CG recomputation. Keep the limitation adjacent to the claim: this is source/record consistency checking, not independently verified numerical proof against a writer who can edit all certificate fields and corresponding digests.

If the required guarantee changes to reject such coordinated certificate editing, the current mechanism is insufficient, as the concrete last row proves. A different assurance mechanism is then necessary: retain and validate a potential witness on the independently rebuilt graph (including topology/plate/current/interval recomputation and source binding), or independently solve. An unvalidated saved phi or a new self-reported hash alone would not close that stronger requirement. That stronger guarantee is not silently imposed here and is not a new pre-seal blocker from this subreview.

## Reproducibility and verification accounting

Run from the supplied repository with the indicated Python interpreter and `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, and TEMP/TMP under this review output.

```text
python -B <graph_review>/probe_graph_core.py
python -B <graph_review>/probe_actual_binding.py
python -B <graph_review>/probe_source_binding.py
python -B scripts/test_carbon_junction.py --only QD,QD2,QD3,QD4,QD5,QD6,QD6x,QD7,QX6,QX35,QG
python -B scripts/test_carbon_junction.py --only FP
python -B scripts/test_ca_ext_b6.py --only S,SGF,Q --skip-payload
python -B scripts/test_ca_ext_b6.py --only SG
python -B scripts/test_step3_target_cert.py --only T25
```

| Execution | Result | Evidence |
|---|---|---|
| Independent core / overflow / exact fingerprint | pass | `graph_core_results.json`, `probe_graph_core.py` |
| Independent real producer / original swap / Q3 / adjacent edits | pass, declared forgery acceptance reproduced | `actual_binding_results.json`, `actual_binding.log`, four `*_manifest.json` files, `actual_assemblies.json` |
| Independent same-code / same-bed boundary probes | pass with explicit argv/settings adapters | `source_binding_results.json`, `source_binding.log`, `probe_source_binding.py` |
| Carbon QD… / QX6 / QX35 / QG | **157/157** | `carbon_relevant.log` |
| Object-array fingerprint FP | **19/19** | `fingerprint_resident.log` |
| B6 S/SGF/Q, payload skipped | **286/286** | `b6_relevant.log` |
| B6 real payload SG/SGF | **10 passed / 1 platform-specific check failed** | `payload_graph_resident.log`: actual full payload and independent graph-only payload both rc 0; graph fingerprints, input binding, contracts, no-solve/no-sigma output, no-upper case, input refusal and write refusal all passed. SG5 alone requires integer peak RSS, but Windows has no Python `resource` module and producer emits `peak_rss_kb=None`, explicitly permitted by the record contract. Environment unit and timing fields matched. No algorithm/source-binding failure. |
| Target certificate T25 | **4/4** | `kcl_resident.log` |
| Additional T24 + T25 attempt | 11 checks passed, one historical comparison blocked by missing Git object `49a1af626` | `target_relevant.log`; not a code failure; T25 separately passed |

These counts are overlapping assertions, not independent experiments to be summed. The direct graph reproduction and separate real payload executions are not presented as full `read_run`/ledger/production-shell-runner execution. Source review confirmed `RunnerGraphSource` at `rint_r_chain.py:4515–4634` uses the same environment constructor, verifies output count/schema/environment/input binding and returns independently assembled graphs; runtime-agent Linux coverage must be reported separately.

Initial missing-dependency/fixture failures were resolved using same-pin files and relevant checks rerun. No full gate, DEM, GPU, real-host campaign, research/S0/R campaign or production operation was run. This review does not close any physical-model limitation or authorize a registered R campaign.

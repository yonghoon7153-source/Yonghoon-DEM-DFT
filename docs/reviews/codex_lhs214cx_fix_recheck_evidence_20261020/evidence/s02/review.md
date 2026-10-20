# Independent S02 adversarial review — 2026-10-20

Review pin: `34713ac9650ece7c8d59b7c4d9a2aefccee693ea`.
Baseline: `685c2bbdbbfee82898a9ec062bb9c2bc94612fc8`.

**Conclusion: S02 can close for the actual Windows support environment tested. No new actionable defect found in this change.** The original unmodified full-suite result is the root agent's `../original_current_boundary.log` and metadata: **40/40, rc0**, versus baseline **23/29, rc1**. This independent probe suite does not replace those original-test logs.

Environment: Windows 11 build 26200; Python 3.12.14; NumPy 2.5.3; SciPy 1.16.3; BLAS/library thread variables set to 1. Test source SHA-256 remains `8af2a5e6041bf26076968b90f54984557f14e9a4b83bf8055c4438d2ca0e99a9`. `network_conductivity.py` and `tau_flux.py` are byte-identical to the baseline. No production/source/git mutations, DEM, or new 214 run occurred. Mutants below exist only in the probe process.

## Search and Windows numerical results

`scripts/test_l214r_r01_restored_full.py:279–305` uses exact equality on independently recomputed real-chain q. The recenter operation at lines 288–290 only chooses a new initial box_y; it is explicitly disclosed and is followed by actual solves. The one-axis search moves monotonically in box_y and stops on an exact target, a crossing, or the 512-step cap. `:316–342` tries areas in the declared deterministic order `0,+1,-1,...,+64,-64` and returns only when all three targets occur at a single area. There is no tolerance change, threshold change, or hidden change to registered `E_AREA`, `E_BX`, or `E_BY` (`:73–78`).

| Start | Fixed-area one-axis result on Windows | First successful second-axis offset | Attempts | Found contact area |
|---|---|---:|---:|---:|
| Registered `0.500000001` | prev skipped | -5 ULP | 11 | 0.5000000009999994 |
| E″a `0.5000000010000005` | next skipped | +2 ULP | 4 | 0.5000000010000007 |
| E″b `0.500000000999999` | next skipped | +1 ULP | 2 | 0.5000000009999991 |

All three found areas produce `I_bottom=0.03976778104389289` in this environment. Found box_y values are respectively `0.7281737983374881`, `0.7281737983374882`, `0.7281737983374883`, giving exact raw q `1.5000000000000002`, `1.5`, `1.4999999999999998`. The latter two remain computed with stored q 1.5; the first is withheld. Original E1–E4 assertions pass. Repeated searches return identical results. All submitted E/E′/E″/E5 sections pass **18/18**.

E″a's missed boundary differs from the author's Linux example. The code and README expressly identify those seeds as Linux observations; the contract requires finding the exact three boundaries in the current environment, not preserving the same skipped target or same successful area.

A fresh sweep of all **401 starting areas** at registered area ±200 ULP found exact boundaries **401/401**. Independent record arithmetic re-read the three produced records for every success. **251/401** needed a second-axis move; maximum absolute move **9 ULP**, maximum **19 attempts**. This is a Windows observation, not a universal guarantee for all solvers/platforms.

Evidence: `core.json`, `core.log`, `sweep.json`.

## Why contact area is a useful second axis

For this chain, all nodes have x=y=0 (`scripts/test_lhs214_model_limit.py:80–83`). The periodic horizontal separations remain zero as either positive box dimension changes (`network_conductivity.py:547–549`). Thus the box dimensions do not change the chain's conductances/current; they enter q through the rounded denominator product (`:1431–1435`). Six actual box combinations, including 0.6×0.9, 0.9×0.6, 0.51×1.04, 1.2×0.45 and 2×0.265, preserve the current bit-for-bit; explicit arithmetic agrees with actual certificate raw q for all six.

At the registered area, `I_bottom=0.03976778104389278`. An independent 129-point actual-producer scan of box_y ±64 ULP repeats the old skip:

| box_y | rounded product box_x×box_y | raw q |
|---:|---:|---:|
| 0.7281737983374861 | 0.530237080585237 | 1.5000000000000002 |
| 0.7281737983374862 | 0.5302370805852371 | 1.5 |
| 0.7281737983374863 | 0.5302370805852371 | 1.5 |
| 0.7281737983374864 | 0.5302370805852372 | 1.4999999999999996 |

Across the scan, product increments are only 0 or 1 ULP, spanning 93 product ULPs with no skipped product double. Enumerating the denominator doubles directly around `(I_bottom*20)/1.5` proves that none produces prev in this neighbourhood: the adjacent denominators yielding 1.5 and 1.4999999999999996 are already consecutive doubles. The division is monotone, and the enumerated endpoints bracket all three targets. Changing box_x cannot supply a missing denominator between them. A separate 401-value box_x ±200 ULP arithmetic sweep also produces zero prev hits.

Therefore the submission's rejection of box_x as a way to fix this particular missing q is justified. The wording that box_y visits “all product doubles” should be read locally for the registered chain/binades; it is not a theorem for arbitrary floating-point products or arbitrary network geometry. Contact area changes the numerator/current and is an effective second degree of freedom here.

The ±64-area bound's 2^-53 grid/three-slot/elasticity motivation remains an empirical explanation, not a solver-accuracy proof or universal portability guarantee. The Windows registered current does satisfy `I_bottom*2^53=358196327781254`, but a platform-independent lattice guarantee is neither required for this closure nor established by these tests.

Evidence: `axis.json` (129 actual scans, denominator enumeration, 401 arithmetic box_x trials).

## Adversarial policy detection and failure behaviour

Production strict comparison stays at `network_conductivity.py:1471`; consumer comparison stays at `tau_flux.py:807`. Six in-process mutants were tested through the new E0 search and the original assertions; the exact-input search continued to succeed, while policy errors were detected:

| Deliberate mutant | Failed original assertion(s) |
|---|---|
| Producer `>` → `>=` | E2, E4 |
| Producer rounds q to 8 places before comparison | E1, E3, E4 |
| Producer FULL guard removed | E1, E2, E3, E4 |
| Consumer `>` → `>=` | E2, E5 |
| Consumer rounds q to 8 places before comparison | E4, E5 |
| Consumer FULL guard removed | E4, E5 |

All four guard-diagnostic keys were also removed from a restored next record; the consumer still rejects it using reconstructed raw q and the policy name. Calling restore on the computed equality record raises the explicit ValueError and leaves the record unchanged (`test_l214r_r01_restored_full.py:146–148`).

With the area bound set to zero in memory, the registered prev cannot be found: E0 and E1–E4 fail explicitly, restoration is never invoked, and E5 passes. A separate full-bound exhaustion probe requests four adjacent targets; all **129** area attempts finish, returning `area=None`, `bys={}` and an explicit scope failure instead of a partial fixture. An injected E search exception produces a failed E section while independent E5 still executes and passes. The separate `_guard` calls are at `:653–659`; E5 remains at `:450–470`.

Evidence: `mutants.json`, `mutants.log`, `failclosed.json`, `failclosed.log`.

## Reproduction and limits

Probe source: `../../probes/s02/adversary.py`. Run using the specified bundled Python with `-X utf8 -B`, followed by one mode: `core`, `axis`, `mutants`, `failclosed`, `sweep`. Each mode writes JSON and captured section logs under this directory. Aggregate independent assertions: **29/29** (core 9, axis 5, mutants 11, failclosed 3, sweep 1).

This demonstrates the declared exact boundary-fixture construction, original Windows test completion, strict policy discrimination, and fail-closed handling. It does not certify the solver's physical accuracy, validate all future environments, rerun A4, or authorize a new 214 launch. E1 mostly confirms the selected premise; E2–E5 attack the policy. The three-node E5 remains the separately constructed exact-boundary control.

# Cascade 9abe5105 release audit

**Frozen source:** `9abe5105cacafa22ab3e185f09e2a4c37118b9a9`  
**Verdict:** **NO-GO for a current 90-species leaderboard, Pareto set, transport shortlist, or winner.**  
**Allowed release:** audit/status page, hash-pinned raw recovery downloads, and five audit figures.

## The four release blockers

### P0-1. The historical 6/6 stop is circular, not an independent transport result

`build_cascade_themes.py` first min-max scales the legacy BVS score, but overwrites that value with `0.05`
whenever the 4 Å foreign-center fraction fails its cutoff. Therefore the displayed `transport_norm=0.05`
is caused by the blocking rule; it is not a second observation that remains low after removing blocking.

Removing only that forced floor while retaining the same historical 47-species BVS scale gives five passes:
Cr2O3 `0.8086`, Ga2O3 `0.3989`, In2O3 `0.6652`, Sc2O3 `0.4868`, Y2O3 `0.8825`.
B2O3 alone remains below the `0.30` cutoff at `0.1000`.

The defensible statement is:

> Six oxidation-onset species stopped at the historical composite G4. Five were stopped by the 4 Å
> foreign-center cutoff, and one by the legacy BVS branch. This does not establish a physical
> oxidation-versus-Li-transport trade-off.

### P0-2. Recovery coverage and evaluable coverage are different denominators

- recovered species with GP records: `90`
- derived ranked rows: `89`
- fully missing species: `AlI3`
- axis-specific missing species: `MgI2` lacks the x005 legacy-BVS input required by G4
- approved current ranking rows: `0`

The phrase “90-species funnel” is prohibited. Even “90 recovered -> 89 evaluated” is only a diagnostic
description because the G3/G4 method contract is not approved.

### P0-3. The 71/18/1 JSON is not a gate-completeness audit

`cascade_pool_audit_v2.json` requires EOS B0 even though historical G1-G5 do not use B0, and omits
Pugh G/B even though G5 does use it. Its `71 complete / 18 partial / 1 dropped` headline measures a
selected five-column ingestion checklist, not funnel completeness.

The axis-specific presence audit is stored in `cascade_audit_gate_completeness.csv`. It keeps missing
separate from fail and never converts an absent x005 value into a G4 failure.

### P0-4. The v2 plot shim is not a release generator

Most legacy plotters still assume O/F-only species, silently fall back from missing v2 inputs to the
historical 47-species files, or write source CSVs from plotting code. In particular,
`plot_cascade_esw.py` can overwrite the recovered 90-species ESW CSV with a hard-coded 47-species table.

No batch regeneration of the legacy 18-figure family is allowed. The default web/PPT whitelist is the
five audit PNG/CSV pairs only. Historical figures remain archive-only.

## Additional contract failures that must stay visible

- All 270 v23 champions have actual `x=0.25`; x002/x005/x010 are directory labels, not 2/5/10%.
- G3 must compare candidate and host inside the same `phase_set_id`; LiS4 inclusion moves the host anchor
  from `2.140` to `2.256 V`.
- The v23 campaign has no usable MLIP-MD sigma or W_ad labels.
- Li2S/LiCl `blocking=0` means “no foreign atom under this implementation,” not an excellent Li channel.
- `ranked_v2`, `themes_v2`, `funnel_v2`, air-axis v2, and the v2 insights image are recovered diagnostics,
  not approved results.
- ML has zero explicit co-doped property labels. It may order validation work, not issue property claims.

## Release decision

The campaign is scientifically useful, but its current product is a **decision contract**, not a winner.
The next expensive calculations should close, in order: same-phase-set GP comparison, canonical low-x
softBV connectivity, matched multi-seed MD at the surviving boundaries, and only then explicit pairs.

The public Cascade page must fail closed: `273 planned / 270 completed / 90 recovered / 47 historical /
0 approved leaderboard / 0 explicit pair labels`.

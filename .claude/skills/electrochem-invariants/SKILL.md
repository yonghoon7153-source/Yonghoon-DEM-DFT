---
name: electrochem-invariants
description: The domain rules that silently corrupt battery data when broken. Read before touching any code that reads a column, computes a capacity, or compares cycles.
when_to_use: Before editing wrdkit, the API's analysis paths, or anything that produces a number a researcher will publish.
---

# Electrochemistry invariants

These are not style preferences. Each one, broken, produces a plot that looks
plausible and is wrong -- the worst failure mode for lab software.

## 1. Time is .NET ticks, not seconds

`DATE TIME`, `TEST TIME`, `STEP TIME`, `CYCLE TIME` are 100 ns ticks.

```python
seconds = wrd.seconds("test_time")   # correct
seconds = wrd.data["test_time"]      # off by 10,000,000x
```

Never divide by `1e7` inline. `wrd.seconds()` exists so the constant lives in
one place.

## 2. Capacity units depend on a flag in the header

`UnitCoulomb` decides whether `CHARGE Q` is amp-hours or coulombs.

```python
mah = wrd.discharge_mah()          # correct, honours the flag
mah = wrd.data["discharge_q"] * 1000   # wrong on a coulomb file
```

## 3. Q columns are per-cycle running totals

`CHARGE Q` resets to 0 at each cycle boundary and holds its final value while
the cell discharges. So:

- **cycle capacity** = the *difference* across the step, not `max()` of the
  column. `segment_steps()` does this.
- **profile capacity** must be re-zeroed at the branch start, which
  `extract_profile()` does.

Taking `max()` over a whole file gives you the largest cycle, not the last one.

## 4. Step boundaries come from `TOTAL STEP`

`TOTAL STEP` is a global monotonic counter. Splitting on it is exact.
Splitting on the current sign is not: a CCCV charge crosses no zero, a rest
step reads zero in both directions, and a GITT pulse train would shatter into
hundreds of fragments.

## 5. `CELL STATUS` is authoritative: 1 rest / 3 charge / 4 discharge

Verified against 148,493 rows of a reference file -- every value agrees with
the current sign. Use it, and fall back to the current only for unknown codes.

## 6. Mean voltage is energy-weighted

```
mean discharge voltage = discharge energy / discharge capacity
```

The arithmetic mean of the voltage samples is not this number, and differs
most exactly where it matters -- a cell with a long low-voltage tail.

## 7. The reference cycle is 3, not 1

Cycles 1-2 are formation. They lose several percent by design (93.2 % CE in
the reference file, against 99.6 % at cycle 3). Anchoring retention or a fade
rate at cycle 1 mixes formation loss into degradation, and makes the early-life
slope so steep that no later knee can exceed it. See ADR 0004.

## 8. Never report a truncated cycle

A file that ends mid-step has a final cycle with a partial capacity. Quoting
it understates the cell. `CycleSummary.complete` marks these; the readout uses
the last complete cycle.

## 9. Zero temperature usually means "no sensor"

The reference file reads 0.0 °C for every row while the chamber was at 60 °C.
Treat an all-zero temperature column as absent, not as freezing.

## 10. Normalised values are never stored

Only raw mAh / Wh / V / A / s go in the database. A mass correction must
re-express every existing number without a re-parse. See ADR 0001.

## Checking yourself

Coulomb-count a cycle and compare against the reported column -- they are
computed independently inside the file, so agreement is real evidence:

```python
mask = current < 0
integrated = np.trapezoid(-current[mask], seconds[mask]) / 3.6  # A·s -> mAh
assert integrated == pytest.approx(cycle.discharge_capacity_mah, rel=0.02)
```

On the reference file this agrees to 0.06 %.

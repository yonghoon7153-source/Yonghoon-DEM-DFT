---
name: verifying-against-a-real-file
description: How to establish that a change to the analysis is correct, rather than merely self-consistent. Run before declaring any numeric work done.
when_to_use: Before saying a parser, analysis or normalisation change is finished.
---

# Verifying against a real file

Unit tests prove the code does what it was told. They cannot prove it was told
the right thing. For anything that produces a physical number, verification
means checking it against something computed a **different way**.

## The checks that actually catch errors

### 1. Coulomb counting vs the reported column

The cycler writes the accumulated capacity *and* the instantaneous current.
Integrating the second must reproduce the first. They come from different
paths inside the instrument, so agreement is real evidence.

```python
mask = current < 0
integrated = np.trapezoid(-current[mask], seconds[mask]) / 3.6
# reference file: 4.9085 vs 4.9114 mAh reported -- 0.06 %
```

### 2. The file must be consumed exactly

`metadata.trailing_bytes == 0`. One leftover byte means the row layout is
wrong somewhere.

### 3. Cut-offs must bracket the measurements

The schedule says 1.88-3.63 V. No sample may sit outside that by more than the
control tolerance. If it does, either the cut-off decoding or the voltage
column is wrong.

### 4. Coulombic efficiency must not exceed 100 % after formation

A cycle that discharges more than it charged is a sign the capacity columns
are being read from the wrong offsets, or that a step was classified backwards.

### 5. Specific capacity must be physically possible

50-400 mAh/g spans every layered oxide. A number outside it means the mass, the
unit flag, or the column mapping is wrong -- and it is almost always the mass.

### 6. Time must advance monotonically

`np.all(np.diff(seconds) >= 0)`.

## Running them

```bash
WRDKIT_SAMPLE=/path/to/real.wrd python3 -m pytest \
  packages/wrdkit/tests/test_real_file.py apps/api/tests/test_real_pipeline.py -q
```

These skip silently without the environment variable, so CI stays green
without a 20 MB file in the repository -- but they are not optional before
declaring work done.

## When a number changes

If a change moves a reported value, put the before/after in the commit message
with the file it came from. A reviewer cannot check a number they cannot see.

```
knee detection: anchor the search at the reference cycle

reference file (No_1_dry_..._012.wrd):
  segmented   23  -> 22
  slope_ratio  -  -> 13   (was undetected: formation set the baseline)
  early fade rate  -0.375 -> -0.081 %/cycle
```

## What does not count as verification

- The tests pass. (They test the code, not the physics.)
- The plot looks right. (A wrong-by-a-constant-factor plot looks right.)
- The number is close to last time. (Both can be wrong.)

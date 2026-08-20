---
name: adding-an-analysis
description: End-to-end recipe for adding a new analysis (EIS fitting, DRT, dQ/dV, coulombic-efficiency trends) so it lands in the same shape as everything else.
when_to_use: Any time a new physical quantity or plot type is requested.
---

# Adding an analysis

The charge/discharge path is the template. Follow its shape and the new
analysis inherits normalisation, export, comparison and grouping for free.

## Before writing anything: the ladder

Ask in order, and stop at the first yes.

1. **Does it need to exist?** Can the question be answered with an existing
   endpoint plus a different basis or filter?
2. **Is it already in `wrdkit`?** `segment_steps`, `extract_profile`,
   `normalize_capacity`, `lttb`, `detect_knee` cover more than they look like.
3. **Is it a pure transform of a cycle table?** Then it belongs in
   `packages/wrdkit/` as a function over `list[CycleSummary]`, not a new
   pipeline.
4. **Does it need new raw columns?** Only then touch the parser.

The best analysis is one that is a thin function over data already parsed.

## The order, and why

```
packages/wrdkit/   pure function + tests        <- always first
apps/api/          router + schema              <- second
apps/web/          page or panel                <- last
```

`wrdkit` must not import FastAPI, SQLModel or anything web. That is what lets
the CLI, the tests and a future notebook use the same code as the app. If a
step needs the database to work, the boundary is in the wrong place.

## Step by step

### 1. ADR

Write `docs/adr/NNNN-<slug>.md` first. One paragraph of context, the decision,
and the cost. If the decision has no cost, it has not been thought through.

### 2. Pure function in `wrdkit`

```python
# packages/wrdkit/src/wrdkit/ica.py
def differential_capacity(profile: Profile, *, smoothing: int = 5
                          ) -> tuple[np.ndarray, np.ndarray]:
    """dQ/dV for one branch. ..."""
```

Rules that keep this reusable:

- Take `Profile` / `CycleSummary` / plain arrays. Never a database row.
- Return raw units. Normalisation is the caller's job (ADR 0001).
- Return `None` plus a reason when the input cannot support the answer --
  see `KneeResult.reason` and `ResolvedCell.missing_for()`.
- numpy only. No scipy: the segmented-regression knee shows that a grid search
  over an exact closed form usually beats a nonlinear optimiser anyway.

### 3. Tests, before the router

Extend `packages/wrdkit/tests/synthetic.py` if the analysis needs a data shape
the fixture cannot produce -- a synthetic curve with a *known* answer is worth
more than any assertion against real data, because it can be wrong on purpose.

Then add the physics check to `tests/test_real_file.py`, which runs only when
`WRDKIT_SAMPLE` points at a real file.

### 4. API

- Response model in `apps/api/app/schemas.py`, carrying its units.
- Route in the matching router; add a new one only for a new noun.
- Accept the same cell-spec override query parameters the other analysis
  routes take, so a what-if mass works everywhere.
- Downsample before returning. `settings.default_plot_points` is the budget.

### 5. Web

- Types in `apps/web/src/lib/types.ts`, mirroring the schema.
- Client method in `lib/api.ts`.
- Reuse `<Plot>`; it already handles a merged x axis, gap spanning, markers
  and the theme. A Nyquist plot is a `<Plot>` with equal axis scales.

### 6. Docs

`docs/log.md` gets one line. `docs/index.md` gets the ADR.

## What "done" means

`make check` passes, **and** the analysis has been run against a real file and
its output sanity-checked against physics -- not just against itself. See the
`verifying-against-a-real-file` skill.

## Planned analyses and where they attach

| Analysis | Attaches to | Needs |
|---|---|---|
| Coulombic-efficiency trend | `CycleRecord` (already stored) | nothing new |
| Cycle-life / retention plots | `CycleRecord` | nothing new |
| dQ/dV (ICA) | `Profile` | differentiation + smoothing |
| dV/dQ | `Profile` | same |
| EIS fitting | a new file type (`.wis`?) | parser work first |
| DRT | EIS spectra | EIS first |

The first two are already possible through `/api/compare/cycles`. Check that
before building anything.

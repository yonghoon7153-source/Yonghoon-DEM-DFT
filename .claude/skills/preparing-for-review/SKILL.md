---
name: preparing-for-review
description: How to shape a change so an external reviewer (Codex, a colleague) can judge it quickly and catch what matters.
when_to_use: Before requesting review on a branch or a PR.
---

# Preparing for review

A reviewer has minutes and no context. The work of review is mostly the
author's.

## One change, one subject

Split a branch that does two things. A reviewer who has to hold two models in
their head checks neither carefully.

## Make the numbers visible

Anything that changes a computed value ships with before/after from a real
file, in the commit message:

```
reference file (No_1_dry_..._012.wrd, 148,493 rows, 45 cycles):
  cycle 44 discharge   3.4172 mAh   (unchanged)
  knee (segmented)     23 -> 22
  early fade rate      -0.375 -> -0.081 %/cycle
```

Without this a reviewer can only check that the code compiles.

## Say why, in the code

The reviewer's hardest question is "why this way and not the obvious way".
Answer it where they will read it:

- an ADR for a decision with consequences,
- a docstring for an algorithm choice (see `knee.py`'s four criteria, and why
  the exact grid search replaced the Bacon-Watts `tanh` fit),
- a comment for a non-obvious line — but only where the code cannot say it.

Do not comment what the code already says.

## Leave the seams visible

Point at the boundary the change crosses:

- `wrdkit` is pure — if this change made it import FastAPI, say why.
- Raw units only in the database — if this stored a normalised number, say why.
- Originals are immutable — if this wrote into `data/uploads/`, say why.

These are the three invariants a reviewer should check first, so make them
easy to check.

## Pre-flight

```bash
make check
WRDKIT_SAMPLE=/path/to/real.wrd python3 -m pytest packages/wrdkit/tests apps/api/tests -q
git diff <base>..HEAD --stat
```

Then read your own diff, top to bottom, as if someone else wrote it. Most
review comments are things the author would have caught on a second read.

## Answering review

Implement, or explain why not — never silently skip. If a suggestion is wrong,
say what it would break, with the case that breaks it.

---
name: extending-the-wrd-parser
description: What to do when a .wrd file fails to parse, or carries a column, control type or format the reader has not seen.
when_to_use: A WrdError, an unknown eCtrlType/eCutoffType, a non-zero eFormat, or trailing_bytes > 0.
---

# Extending the .wrd parser

The format has no public specification. `docs/raw/specs/wrd-binary-format.md`
is what we established by decoding real files, and it is the contract the
parser and the synthetic fixture both implement.

## First: what does the file actually say?

```bash
PYTHONPATH=packages/wrdkit/src python3 -m wrdkit.cli info suspect.wrd
```

Then the two strong tells:

- **`trailing_bytes > 0`** — the row scan stopped early. Either the row layout
  is wrong, or there is a footer stream after the data.
- **an unknown enum** — a step prints as `Type9` instead of `CC`/`CCCV`.

## Rules that keep the parser honest

1. **Never hard-code the column layout.** It is computed from the column list
   the file declares. A new column appears in `WrdMetadata.columns`
   automatically; only its *meaning* needs a name in `_COLUMN_ALIASES`.
2. **Fail loudly on the unknown.** `NrbfError` on an unknown record type is
   deliberate — a silent skip would shift every following offset and produce
   numbers that look fine.
3. **Record what you learn.** A new enum value goes in three places: the enum
   class in `schedule.py`, the spec document, and `synthetic.py`.
4. **The fixture is the proof.** If `synthetic.py` can write a file with the
   new feature and the reader reads it back, the spec is right. If you cannot
   write it, you do not understand it yet.

## Adding an enum value

```python
class ControlType:
    CC = 0
    CV = 1
    REST = 7
    CCCV = 13
    NAMES = {0: "CC", 1: "CV", 7: "Rest", 13: "CCCV"}
```

Establish the meaning from the data, not from the number: filter the rows of a
step with that control type and look at the current and voltage traces. A step
whose current is constant and whose voltage ramps is CC. Write down in the spec
*how* you established it, not just the conclusion.

## Adding a column

1. Add the slug to `_COLUMN_ALIASES` in `wrd.py` so it gets a stable name.
2. Add it to `DEFAULT_COLUMNS` in `synthetic.py` and to `Sample.pack()`.
3. Add its .NET type to `_DOTNET_DTYPES` if it is not already there.
4. Update the column table in the spec.

## A new `eFormat`

Format 0 is the cycling layout. Another value means a different file kind
(EIS, most likely). Do **not** try to read it with the same row layout.
Raise a clear `WrdError` naming the format, and open an ADR before building a
second reader.

## Verifying a change

```bash
python3 -m pytest packages/wrdkit/tests -q
WRDKIT_SAMPLE=/path/to/real.wrd python3 -m pytest packages/wrdkit/tests -q
```

The second run adds the physics checks. Both must pass, and
`trailing_bytes` must be 0 on every real file you have.

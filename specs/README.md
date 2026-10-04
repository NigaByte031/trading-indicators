# Specifications

This folder is the **single source of truth** for every indicator in the
repository. A specification is written in plain language and is independent of
any programming language; each port must follow it exactly.

## Files

- `specs/<slug>.md` — the human-readable specification of one indicator.
- `specs/vectors/<slug>.json` — machine-readable test vectors shared by every
  language port.

## Spec template

Copy this into `specs/<slug>.md`:

```markdown
# <Indicator name> (<ABBR>)

One-sentence description.

## Parameters

| Name   | Type | Default | Range   | Description |
|--------|------|---------|---------|-------------|
| period | int  | 14      | >= 1    | ...         |

## Input

- `close` — the input price series (numbers, oldest first).

## Output

- `abbr` — a series the **same length** as the input.
- Describe leading undefined values and how the series is seeded.

## Algorithm

Numbered, unambiguous steps. Include the exact constants and the seeding rule,
because seeding differences are the most common source of divergence between
languages.

## Edge cases

- period out of range -> error
- period longer than the input -> ...
- period == 1 -> ...

## References

Links to the original definition if applicable.
```

## Test vector format

`specs/vectors/<slug>.json`:

```json
{
  "indicator": "<slug>",
  "spec": "<slug>.md",
  "cases": [
    {
      "name": "human readable description",
      "parameters": { "period": 4 },
      "input": { "close": [10, 12, 11, 13] },
      "expected": { "abbr": [null, null, null, 11.5] }
    }
  ]
}
```

Rules:

- `null` in `expected` means an **undefined** output value (NaN).
- Floating point results are compared with a small tolerance (see each test
  runner), so store a sensible number of significant digits.
- Prefer a couple of cases per indicator: a normal one, a boundary one, and one
  that exercises the seeding rule.

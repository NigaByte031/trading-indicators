# Pull request

## What does this change?

<!-- A one or two sentence summary, and the motivation behind it. -->

## Checklist

- [ ] This follows the **spec-first** workflow in
      [`CONTRIBUTING.md`](../CONTRIBUTING.md): the specification is the source
      of truth and every port must agree with it.
- [ ] If an indicator changed, its spec in `specs/<slug>.md` was updated.
- [ ] If an indicator changed, its shared vectors in `specs/vectors/<slug>.json`
      were updated.
- [ ] Every affected language port was updated in the same change.
- [ ] Tests load the shared vectors (no hard-coded expected values).
- [ ] `cd python && python -m pytest` passes.
- [ ] `cd python && ruff check .` passes.
- [ ] The indicator matrix in the root `README.md` is up to date.

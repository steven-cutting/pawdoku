---
title: "Decision 0011: Executable models of specifications"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_executable_prototypes]
requires: []
---

# Decision 0011: Executable models of specifications

*This game's first decision of its own. The ten before it came with the template.*

## Context

`docs/specs/board.allium` was specified before any of it was built, as
[Decision 0003](0003-specs-are-the-source-of-truth.md) requires. A specification of that
size — four moves, exact undo and redo, reading back, checks and a record — is easy to
write consistently and hard to know is consistent, and the application it will be
implemented in does not exist yet to try it against.
[Decision 0004](0004-python-toolchain.md) keeps a Python toolchain in the repository for
the hook gate and the two validators, and said the game shipped no Python of its own.

## Decision

A specification may be made executable under `prototypes/` before the application
implements it. `prototypes/board/` models `board.allium` in Python with `attrs`, its cells
typed values, and pytest scenarios that render the board as text into an
`inline-snapshot` after every step, holding every named invariant of the module and of
`sudoku.allium` after every stimulus. The three packages sit in the `proto` dependency
group of `pyproject.toml` and `mypy` in `dev`, each pinned exactly and locked like the
rest. `just proto-typecheck` holds the model under `mypy --strict`, where two of the
specification's invariants are proved from the types rather than held at run time;
`just proto-test` runs it; both are gates in `just check`. `just proto-accept` rewrites
the snapshots to what the model now renders, and is run only after the renderings have
been read, because they are the review.

A model is imported by nothing, is never built and never reaches the published site. It
is the specification exercised, not the application tested: `tests/` and the coverage
floor over `src/lib/**` are the application's evidence and stay as they were.

## Consequences

Python is now real code this repository lints, so Ruff runs over `prototypes/` with the
rules `pyproject.toml` relaxes for its tests, and the Markdown fences Ruff would also
format are excluded from `just format`. The local gate is longer by the model's run. CI
runs neither `proto-typecheck` nor `proto-test`: the shared workflow `ci.yml` calls is
pinned at a release that predates both recipes, so until a release carries them a red
model merges green and `just check` is where it is proved;
[Quality gates](../reference/quality-gates.md) says so.

A model can drift from its specification as quietly as an implementation can. The
specification moves first and the model follows it in the same change, under the
`spec-change` skill's discipline; the model is never the reason a clause changes.

## What would reopen this

The board landing in TypeScript under `src/lib/`, when the model has served its purpose
and would either be kept current for nothing or deleted; or the shared workflow gaining a
way to run a game's own recipes, which would move both into CI and close the gap above.

## Related pages

- [Decision 0004: A Python toolchain in a frontend repository](0004-python-toolchain.md)
- [Repository map](../project/repository-map.md)
- [Quality gates](../reference/quality-gates.md)
- [Testing](../reference/testing.md)

---
title: "Quality philosophy"
kind: "explanation"
audience: [contributor, maintainer, agent]
canonical_for: [quality_philosophy]
requires: []
---

# Quality philosophy

Gates encode decisions, not taste. Each one exists because someone decided something, and
the gate is what stops the decision quietly reverting. If a gate cannot be traced back to
a decision, it should be deleted rather than tolerated.

## Checks are read-only

Every recipe under `just check` reports and never repairs. Recipes outside it do write —
`just format`, `just initialize` and the lock recipes among them — and `just fix` is the
one whose job is repairing what a check reported. `bg-project-check`, the runner behind
`just check`, enforces the split by snapshotting every path Git does not ignore and
comparing after every recipe, so a check that rewrites a file fails the run rather than
hiding drift.

This is why the pre-commit configuration is split in two. `.pre-commit-config.yaml` is
the gate and is what gets installed; `.pre-commit-fix.yaml` holds the mutating hooks and
runs only from `just fix`.

## Fix the cause, not the report

A suppression is a last resort: one rule, one line, with a stated reason. Lowering the
coverage threshold, disabling a lint rule at a call site, or loosening an assertion until
it passes are all ways of deleting the signal while keeping the machinery.

Where a rule is genuinely wrong for this project, the fix is to configure it once, in the
config file, with a comment saying why. `eslint.config.js` carries no such override
today: `strictTypeChecked` applies as shipped, so a number reaching a template literal
has to go through `String()` at the call site, because there is no `allowNumber`
exception to let it through bare. The first override this game adds is a project
decision, recorded where the rule lives.

## Unreachable is not untested

Coverage distinguishes two things that look alike. A branch no input can reach is not a
gap in the tests; it is code that should not exist, whether a bounds check after a
modulo, a null fallback after an exhaustive assignment, or a defensive default no caller
can trigger. Delete it rather than cover it with a contrived test.

The corollary: do not chase the last few percent. The floor is 90, and in a fresh render
the denominator is small, three ports and about fourteen branch sites, so an untested
constants file or a branch in a component nothing renders can breach the floor on its
own.

## Tests inject, they do not stub

A fake is not a mock. It behaves — the fake clock advances, the fake storage remembers,
the fake random walks a sequence you chose. Tests that assert a function was called are
not evidence that anything works.

Stubbing a global is banned outright, and the design makes it unnecessary: every adapter
takes its platform object as a defaulted argument. This turned out to matter more than
expected, because the test environment provides no `localStorage` at all.

## The specification is the arbiter

When a test and the code disagree, one of them is wrong and the specification says which.
Neither is adjusted until it passes.

## Related pages

- [Quality gates](../reference/quality-gates.md)
- [Testing](../reference/testing.md)
- [Specifications](specifications.md)

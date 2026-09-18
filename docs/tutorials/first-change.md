---
title: "Make your first change"
kind: "tutorial"
audience: [contributor, agent]
canonical_for: [first_change_tutorial]
requires: []
---

# Make your first change

About half an hour, from a fresh clone to a green gate — the first run downloads a browser
and reads one package from GitHub Packages, which needs a token in `~/.npmrc` that
[Develop locally](../how-to/develop-locally.md) describes.
The change is small on purpose; what matters is that it passes through every layer the
repository has.

## 1. Get the workspace running

```console
just initialize
just check
```

`just initialize` creates the lockfiles, installs both toolchains, downloads the Chromium
build the story gate renders in, normalises formatting and installs the pre-commit hook. It
never stages, commits, tags or pushes. If it complains about a missing tool, read
[Develop locally](../how-to/develop-locally.md).

## 2. See the app

```console
just dev
```

Open the address it prints. You will see the platform's header carrying this game's lockup,
and a main landmark with a short placeholder in it. The lockup's words come from
`src/lib/brand.ts`, the one place the game's name is written.

## 3. Read what decides the behaviour

Open the one module under `docs/specs/`, named after this game's slug, and find the `Play`
surface and its guarantee. The `config` block above it restates six figures the platform
states, and `src/lib/config.ts` mirrors them; `tests/platformSpecs.test.ts` holds the three
equal, so a figure changed in one place and not the others fails the gate rather than
drifting.

## 4. Change something

Decide what the main landmark should say instead of its placeholder. Add a case to
`tests/route.test.ts` that queries the `main` landmark by role and asserts the new words,
then run the suite and watch it fail — which is the point.

```console
just frontend-unit
```

A test that is green before you have changed anything is either already covered or vacuous.

## 5. Add the behaviour and its test together

Change the placeholder in `src/routes/+page.svelte`, run the suite again, and land the
component change and the assertion in the same commit. Pick something this game owns: the
cells, the keys and the primitives are the platform's, and their wording is amended upstream
rather than here. The rule holds for every later change: a component change and its Testing
Library assertion land together, and the assertion queries by accessible role and name.

## 6. Run the whole gate

```console
just check
```

It runs every recipe in order and proves the run did not modify the worktree. Read only
the first failure; the later ones are often consequences. If a gate fails, do not work
around it — [Troubleshooting](../operations/troubleshooting.md) covers the common causes.

## 7. Commit

The pre-commit hook runs the read-only gate again. Nothing is pushed until you ask for it.

## What you just touched

A specification you read, a test, a component, and the gate. That is the whole loop; every
change after this one is the same shape, and the first real one starts by adding a rule to
the module rather than reading it.

## Related pages

- [Develop locally](../how-to/develop-locally.md)
- [Test and debug](../how-to/test-and-debug.md)
- [Work with the specifications](../how-to/work-with-the-specs.md)

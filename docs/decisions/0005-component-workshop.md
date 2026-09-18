---
title: "Decision 0005: A component workshop"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_component_workshop]
requires: []
---

# Decision 0005: A component workshop

*Carried from Poodl's decision 0006 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*

## Context

The specifications name surfaces, and every component that renders one is an
accessibility contract as much as a rendering job: a shape for every mark, a name for
every control, a keyboard path to every operation, and two palettes to satisfy.

Nothing in the repository renders a component on its own. A component is reachable only
through a route, and the states that matter are reached by playing the game until it
produces them. The component tests assert accessible names in jsdom, which is exactly the
right evidence and is not something anybody looks at.

## Decision

Add Storybook as a local component workshop. Stories live in a root-level `stories/`
directory, written in Svelte CSF as `*.stories.svelte`, one file per component, covering
the states its surface names.

`@storybook/addon-vitest` renders every story in real Chromium through Playwright, and
`@storybook/addon-a11y` runs axe over each one in the same pass, failing the run on a
violation rather than filing a note. Toolbar globals set `data-theme` and
`data-high-contrast` on the root element, which is what the platform's stylesheet keys on,
so both palettes are one click apart before the settings surface exists.

The workshop is local: a recipe serves it, two recipes gate it, and the Pages
workflow is untouched. What publishes it is `just chromatic` and a workflow of its
own, for visual review — [Decision 0006](0006-visual-review-in-chromatic.md).

## Consequences

Every state of a component becomes a thing you can open, in either palette, and the
accessibility check for it runs without anyone remembering to ask for it.

One lesson from Poodl's workshop is worth carrying without its history. A gate's silence
is not a pass: axe's contrast rule downgrades any element whose visible text is a single
character to *incomplete* and reports incomplete without failing, so a board of one-letter
cells is never in scope for it; and a figure recorded in prose beside a colour drifts from
the colour, so a colour this game adds needs a measurement of its own rather than a number
in a comment.

The dependency surface grows sharply in a repository that pins every version by hand. Each
direct package is pinned exactly, as invariant 4 requires, but the transitive tree under
Storybook is held by `package-lock.json` and by nothing else. Two consequences are worth
naming: the autodocs addon depends on React, which now lives in the tree although it never
enters `src/` or the build; and the Svelte framework package pins TypeScript to a 5.x
line, so npm nests a second copy of the compiler beside the 6.x one this repository uses.

The story run needs a real browser, and a real browser is in neither lockfile. Playwright
downloads a Chromium build over the network into a cache outside the repository, versioned
by the `playwright` pin rather than by anything `package.json` records. This repository
prefers evidence that runs offline, and this is the first check that does not. It is
accepted because axe on a real browser reports contrast, landmarks and computed names that
a jsdom render cannot produce at all.

It is not the only request. The workshop composes the platform's published one
through a Storybook `refs` entry, so `just storybook-build` makes a request of its
own every time the gate runs. The difference from the download above is that this
one cannot fail: an unreachable address degrades to a sidebar entry that does not
open. [Quality gates](../reference/quality-gates.md) states the exception.

Component behaviour is now expressed in two places: an assertion in `tests/` and a fixture
in `stories/`. They can disagree, and when they do neither is the arbiter — the
specification is, as it was already. Each story cites the surface and the `@guarantee`
clauses it stands for by name, so a story says which authority it answers to rather than
becoming one.

Coverage is unaffected on purpose. The floor over `src/lib/**` is measured from the jsdom
suite alone, and the story run lives in its own Vitest configuration with no coverage
block, so a story that renders a component cannot make that number look better than the
tests have earned.

Everything Storybook writes is ignored by Git, because a gate that changes one byte of the
worktree fails the run before its own exit code is read.

## What would reopen this

The Svelte CSF addon falling behind a Svelte major, which would make the story format the
reason not to upgrade the framework. Storybook majors moving past the Vite and Svelte line
this repository pins. Or the game's surfaces getting built and the workshop costing more
to keep than it returns — it is a tool for building, and a tool that has finished its job
can be deleted.

## Related pages

- [Work in the component workshop](../how-to/work-in-the-component-workshop.md)
- [Testing](../reference/testing.md)
- [Accessibility](../explanation/accessibility.md)

---
title: "Specifications"
kind: "explanation"
audience: [contributor, maintainer, agent]
canonical_for: [specification_model]
requires: []
---

# Specifications

This game's behaviour is written down, in a formal language, before it is built. The
Allium modules under `docs/specs/`, rooted at the module named after this game, are the
source of truth for what the game does. This handbook, the code and the tests all answer
to them.

The procedure is in [Work with the specifications](../how-to/work-with-the-specs.md).
This page is why.

## What a specification is for

A figure looks like a detail and is not. The smallest a control may be is stated once, in
`operation.allium`'s `config` block, as 44 CSS pixels. This game's root module restates
it by name, `src/lib/config.ts` mirrors it once, and `tests/platformSpecs.test.ts` holds
the three equal, so a story that measures its controls against `MINIMUM_TOUCH_TARGET`
fails a control drawn at 40 pixels on the number rather than on a reviewer's eye. The
measuring is each story's to do: the seed story measures the header's controls, and axe
holds a control to no more than WCAG's 24 pixels, so a control no story measures is held
to nothing stricter. Left to prose, a figure like that drifts. Stated as a contract with a
named guarantee, it is testable.

## What the modules are

One is the game's today: the root module under `docs/specs/`, named after this game,
which [the documentation map](../README.md) names. It states the six figures the
platform states, so `tests/platformSpecs.test.ts` can hold the two equal, and one
surface with one guarantee, so the specification is checked rather than merely
present. Modules this game adds import it. The platform's own three,
`appearance.allium`, `operation.allium` and `play-surfaces.allium`, ship inside
`@steven-cutting/biscuit-games` and are not imported: Allium has no cross-repository
import, so a clause this game restates is held to the platform's text by test instead.

## Open questions are a feature

An `open question` block records a product decision nobody has made yet. They are
recorded rather than resolved on purpose: an unwritten gap gets filled in by whoever
writes the code first, silently and invisibly, while a written one has to be answered by
someone entitled to answer it.

A low count is the normal state of a settled module, not a reason to stop using the
construct. A change that reaches a decision nobody has taken should add one rather than
guess.

## What a specification is not

It is not a design document, and it does not choose a language, a framework, a storage
mechanism or a layout. A module states what any implementation must satisfy and describes
no scheme for satisfying it. How is this repository's business; `AGENTS.md` decides that.

## Related pages

- [Work with the specifications](../how-to/work-with-the-specs.md)
- [Accessibility](accessibility.md)
- [Decision 0003](../decisions/0003-specs-are-the-source-of-truth.md)

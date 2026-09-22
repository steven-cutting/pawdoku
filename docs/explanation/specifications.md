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

Eight are the game's today. The root module under `docs/specs/`, named after this game,
which [the documentation map](../README.md) names, states the six figures the
platform states, so `tests/platformSpecs.test.ts` can hold the two equal, and one
surface with one guarantee, so the specification is checked rather than merely
present. `sudoku.allium` states the rules of classic Sudoku — the grid, what a setter
may pose, what a player may do and when a puzzle is solved — and nothing about how any
of it looks, so it imports nothing; a module that draws the rules imports both.
`solver.allium` states what `sudoku.allium` leaves a black box: the search that gives a
set of givens its verdict — no solution, one or many — and the work that search may be
seen to do, and nothing about how it is stored or made fast. It imports the rules and is
not imported by them.

Five more say how a person solves a puzzle, which `solver.allium` excludes.
`technique.allium` states the named techniques once — when each holds on a grid of digits
and candidates and what it places or strikes — and the profile of a player: what they
know, how much they hold in mind, how much of the grid they take in, and whether they
keep marks. Four models stand on it and never import each other, because
each is a different answer to what a limit does. In `reach.allium` a limit hides a
deduction, so a puzzle is within a player's reach or it is not, and the next thing that
player would find is a hint pitched at them. In `effort.allium` a limit makes a deduction
dear, and a puzzle is priced end to end. In `lapse.allium` a limit lets marks fall
behind until the player guesses, and a guess is the one thing that can be wrong.
In `human-solving.allium` a limit changes what is noticed, kept in mind and got wrong,
by chance: it specifies independently tunable cognition, experience, aids, fallible
microsteps and seeded repeated assessments, and the projection from its finer
description of a player to `technique.allium`'s profile, so that one player can be put
through all four and the results compared.
`technique.allium` defines 29 techniques, including bounded chains and explicit
uniqueness premises, and records how each question it once left open was resolved.
`lapse.allium` records the same of its own seven, each answer deliberately simpler than
`human-solving.allium`'s. `effort.allium` remains coarse and retains its open questions,
which name the answer `human-solving.allium` gives where it gives one. Its [owning explanation](human-solving.md) states the
research basis and provisional parameter choices. These are behavioural contracts
for a future simulator; passing the Allium gates is not an empirical validation.
The platform's own three,
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
- [Modelling a human Sudoku solver](human-solving.md)
- [Decision 0003](../decisions/0003-specs-are-the-source-of-truth.md)

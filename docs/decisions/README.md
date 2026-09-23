---
title: "Architecture decisions"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_index]
requires: []
---

# Architecture decisions

A record of what was chosen, what it cost, and what would have to change for the choice
to be revisited. Each entry is numbered and never renumbered; a decision that is
superseded is marked rather than deleted, because the reasoning is what makes the
successor legible.

These are decisions about *how* Pawdoku is built. Decisions about *what* it does belong in
the specifications under `docs/specs/`, and unresolved ones are recorded there as
`open question` blocks — see [Specifications](../explanation/specifications.md).

## The record

| Number | Decision |
| --- | --- |
| [0001](0001-static-site-no-backend.md) | A static site with no backend |
| [0002](0002-ports-and-fakes.md) | Side effects behind ports |
| [0003](0003-specs-are-the-source-of-truth.md) | Specifications decide behaviour |
| [0004](0004-python-toolchain.md) | A Python toolchain in a frontend repository |
| [0005](0005-component-workshop.md) | A component workshop |
| [0006](0006-visual-review-in-chromatic.md) | Visual review in Chromatic |
| [0007](0007-project-managed-allium-cli.md) | A project-managed Allium binary |
| [0008](0008-design-system-as-a-package.md) | The design system arrives as a package |
| [0009](0009-rendered-from-the-template.md) | Rendered from the template |
| [0010](0010-a-project-pages-site.md) | A project Pages site |
| [0011](0011-executable-prototypes.md) | Executable models of specifications |

## The numbering

The first ten entries came with the template this game was rendered from, and eight
of them were carried from Poodl, the first Biscuit Games game. Each of those says so
under its heading and keeps the topic slug it had, because the slug is what a
cross-repository reference names. The template never adds, renames or retitles a
numbered decision after its first release, because this directory is the game's from
the first commit and a template update never touches it;
[Decision 0009](0009-rendered-from-the-template.md) says why. A decision this game
takes is numbered 0011 onward and never collides with one the template ships.

## Writing a new one

Copy the shape of an existing entry: context, the decision, the consequences including
the ones that hurt, and what would reopen it. Add the file, add a manifest entry, add a
row above. A decision nobody can find is not recorded.

## Related pages

- [Documentation map](../README.md)
- [Architecture](../explanation/architecture.md)

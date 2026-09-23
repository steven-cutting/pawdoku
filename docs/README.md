---
title: "Documentation map"
kind: "project"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [documentation_navigation]
requires: []
---

# Documentation map

Every page below is registered in `manifest.yml`, owns at least one topic, and is
reachable from here. That is the whole of the arrangement; the rules behind it are in
[Documentation contract](reference/documentation-contract.md).

Behaviour is specified separately, in Allium, under `docs/specs/`, rooted at
[`pawdoku.allium`](specs/pawdoku.allium), with the rules of Sudoku themselves in
[`sudoku.allium`](specs/sudoku.allium), the puzzle in play — its notes, moves, undo and
check — in [`board.allium`](specs/board.allium), and what decides whether givens are
well-posed in [`solver.allium`](specs/solver.allium). How a person solves one is
[`technique.allium`](specs/technique.allium)'s, with four models of a player built on it:
[`reach.allium`](specs/reach.allium), [`effort.allium`](specs/effort.allium),
[`lapse.allium`](specs/lapse.allium) and
[`human-solving.allium`](specs/human-solving.allium), the one with chance in it: bounded
cognition, fallible attempts and repeated assessment. Three more modules are the
platform's, arrive inside `@steven-cutting/biscuit-games`, and are compared against this
game's restatements rather than edited here; see
[The platform upstream](project/platform.md). Those files are not part of this handbook;
they are its subject. Start at [Specifications](explanation/specifications.md) to
understand how the two relate.

## Start here

- [Purpose and scope](project/purpose-and-scope.md) — what Pawdoku is for, and what it is not.
- [Repository map](project/repository-map.md) — where everything lives.
- [Terminology](project/terminology.md) — the words this repository uses precisely.
- [Make your first change](tutorials/first-change.md) — clone to green gate, once through every layer.

## How to

- [Develop locally](how-to/develop-locally.md)
- [Test and debug](how-to/test-and-debug.md)
- [Work in the component workshop](how-to/work-in-the-component-workshop.md)
- [Work with the specifications](how-to/work-with-the-specs.md)
- [Maintain dependencies](how-to/maintain-dependencies.md)
- [Deploy to GitHub Pages](how-to/deploy-to-github-pages.md)
- [Update from the template](how-to/update-from-template.md)

## Platform

- [The platform upstream](project/platform.md) — what Biscuit Games decides for this game,
  which version of it is installed, and where to read the rest.

## Understand

- [Architecture](explanation/architecture.md) — how a static site with no server is put together.
- [Layering and dependency direction](explanation/layering.md) — which module may import which.
- [Specifications](explanation/specifications.md) — why behaviour is written down before it is built.
- [Accessibility](explanation/accessibility.md) — the obligations the specifications state.
- [Security model](explanation/security-model.md) — what a site with no backend does and does not defend.
- [Quality philosophy](explanation/quality-philosophy.md) — why each gate exists.

## Look up

- [Commands](reference/commands.md)
- [Configuration](reference/configuration.md)
- [Testing](reference/testing.md)
- [Quality gates](reference/quality-gates.md)
- [Documentation contract](reference/documentation-contract.md)
- [Agent contract](reference/agent-contract.md)

## Run it

- [Maintenance](operations/maintenance.md)
- [Troubleshooting](operations/troubleshooting.md)

## Decisions

- [Architecture decisions](decisions/README.md) — the record of what was chosen and why.

## This game

Pages this game adds are listed here, after everything the template manages, so an
update from the template and an addition here land in different places.

- [Strategies for solving Sudoku](explanation/solving-sudoku.md) — how people, mathematics and
  programs solve one, and the background to [`solver.allium`](specs/solver.allium).
- [Modelling a human Sudoku solver](explanation/human-solving.md) — cognitive limits,
  experience, mistakes, parameter presets and profile-relative assessment.

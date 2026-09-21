---
title: "Terminology"
kind: "project"
audience: [contributor, maintainer, operator, agent]
canonical_for: [project_terminology]
requires: []
---

# Terminology

These words mean one thing here. Most of them come from the specifications, and using
them loosely is how a review ends up arguing about vocabulary instead of behaviour.

## The game

The game adds a row for every term its specification names. The Sudoku terms are
`sudoku.allium`'s, which picks one word where the game's literature has several, the
solving terms are `solver.allium`'s, and the terms of a person solving are
`technique.allium`'s, its three baseline models' and `human-solving.allium`'s.

| Term | Meaning |
| --- | --- |
| Player | Whoever is at the device. One at a time, and nothing here knows of a second. |
| Play surface | Where Pawdoku is played: the platform's cells and keys in an arrangement this game decides. `Play` is its name in the root module. |
| Puzzle | One game of Sudoku: a grid, the givens its setter supplied, and whether it is solved. |
| Setter | Whoever or whatever supplies a puzzle's givens. The rules say what it may pose, never how it finds one. |
| Cell | One position of the grid, at a row and a column, holding a digit or empty. A rules concept: the platform's play cell is what draws one. |
| Digit | 1 to 9. The only thing a cell holds. |
| Box | One of the nine 3 by 3 squares that tile the grid. Never block, region or subgrid. Its band counts boxes from the top and its stack from the left. |
| Unit | A row, a column or a box: nine cells that must end up holding nine different digits. |
| Peer | Another cell sharing a unit with this one. |
| Given | A digit the setter wrote in before play. The player can never change it. Never clue. |
| Well-posed | Having exactly one solution. Every puzzle a setter may pose is. Never proper. |
| Conflict | Two peers holding the same digit. The rules permit it and both cells are in it. |
| Solved | Every cell holds a digit and none conflicts. Final: a solved puzzle takes no more moves. |
| Candidate | A digit a cell may still hold while givens are being solved. `solver.allium`'s, as are the seven terms below. |
| Search | The solving of one set of givens, from the moment they are handed over to its verdict. |
| Branch | One grid of candidates within a search. One works at a time, and a guess splits it into a child for each candidate of one cell. |
| Propagate | To strike a placed digit from its peers' candidates and place the singles that leaves, until nothing more follows. |
| Guess | A digit tried in a cell when propagation has run out, and the branch opened to try it. Never trial or assumption. |
| Contradiction | A branch that can hold no solution: a cell with no candidate, a unit with no place for a digit, or a cell that is the only place for two digits. |
| Verdict | What a search concludes of its givens: none, one or many solutions. One is well-posed. |
| Solution | A full grid with no conflict that holds every given. What a solved branch holds. |
| Technique | A named way a person deduces something from a grid: a full unit, a cross-hatch, a naked or hidden single, pointing, claiming, a naked or hidden subset, and the rest of `technique.allium`'s catalogue. |
| Ladder | The order techniques are tried in, cheap and local before dear and global. A technique's rank is its place on it. |
| Deduction | One place a technique holds on a grid: where, with which digits, and what it places or strikes. |
| Placement | A digit a deduction, or a guess, puts in a cell. |
| Strike | Candidates a deduction removes from a cell. Never eliminate. |
| Mark | A candidate as the player has it written. Stale when a placed peer rules it out; lapsed marks are marks left stale. |
| Subset | A pair, a triple or a quad, naked or hidden. |
| Cross-hatch | A hidden single read from the placed digits alone, with no marks, in a box or a line. |
| Pointing, claiming | A box whose places for a digit lie on one line, and a line whose places lie in one box. Never box-line reduction. |
| Profile | A parameterized player. The baseline `technique/Profile` has repertoire, capacity, spans, marking, order, fixation, upkeep, budget, fatigue and patience. The richer `human-solving/PlayerProfile` separates ability, experience, biases and coping. |
| Load, capacity | Baseline load is a coarse per-proof figure. In the richer model capacity bounds simultaneously retained chunks, including pending reasoning and unwritten branch data. Neither is a count of Sudoku cells or an intelligence score. |
| Extent, span | How much of the grid a deduction is read across, and an extent a player takes in. |
| Run | One player model put to one set of digits. It looks, steps and looks again. Each model has its own. |
| Step | A deduction taken; in `lapse.allium` also a check, a guess or a repair. |
| See, stall | In `reach.allium`: a deduction the profile does not hide is seen, and a run that sees nothing in an unfilled grid stalls. |
| Price, escalation | In `effort.allium`: what a step costs this player, and a step taken from beyond their profile. |
| Check, repair | In `lapse.allium`: bringing every mark up to date, and returning the grid to how it stood before a wrong guess. |
| Attempt | In `human-solving.allium`: one fresh puzzle, resolved profile, environment, budgets, versions and seed, carried through to a stopping reason and independent judgement. |
| Microstep | One paid action such as attending, inspecting a fact, rehearsing, inferring, writing a note or committing a digit. An unsuccessful action is still recorded. |
| Fact, belief | One proposition acquired or derived by the simulated person. It has provenance and confidence and can be false; a coverage assertion does not contain all the facts it summarizes. |
| Chunk | A bounded group of learned, recognized facts occupying one working-memory slot. Arbitrary bundles do not qualify. |
| Sheet | Actual entries, external candidate notes and deliberately written branch records, separate from mental beliefs and observer knowledge. |
| Coverage | An assertion that all alternatives of one cell, or all positions for one digit in a unit, were checked. Missing partial notes do not establish coverage. |
| Observer | The independent evaluator that can inspect full traces and solution truth; its judgements do not steer the simulated person. |
| Assessment | Results from a declared seed list under one fixed condition, retaining counts, distributions and every attempt rather than a universal scalar difficulty. |
| Familiar recognition, elementary derivation | A learned pattern shortcut, and explicit reasoning from acquired Sudoku premises. Deriving an unfamiliar pattern does not make it familiar. |
| Fatigue, frustration | Bounded transient states altered by spent effort, fruitless search, perceived progress and rest; independent of fixed experience. |

## The repository

| Term | Meaning |
| --- | --- |
| Specification | An `.allium` file under `docs/specs/`. Decides behaviour. |
| Surface | A boundary in a specification: what is exposed, what operations are provided, and what is guaranteed. |
| Guarantee | A named prose assertion on a surface. Acceptance criteria, not aspiration. |
| Port | An interface standing in front of a side effect, with a real adapter and an in-memory fake. Three are in `src/lib/ports/`; the device's preferences and its keyboard are the platform package's. |
| Platform | Biscuit Games: the repository that decides everything Pawdoku would share with another game. See [The platform upstream](platform.md). |
| Exact | The platform's name for a mark that is wholly right, after the token that paints it. A game whose rules use another word translates it where a mark reaches something rendered. |
| Fake | The in-memory implementation of a port, used by tests. Not a mock: it behaves, rather than recording calls. |
| Gate | A check that can fail the build. Listed in [Quality gates](../reference/quality-gates.md). |
| Recipe | A `Justfile` target. The only supported interface to the checks. |

## Related pages

- [Specifications](../explanation/specifications.md)
- [Modelling a human Sudoku solver](../explanation/human-solving.md)
- [Repository map](repository-map.md)

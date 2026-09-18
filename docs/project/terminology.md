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
`sudoku.allium`'s, which picks one word where the game's literature has several.

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
- [Repository map](repository-map.md)

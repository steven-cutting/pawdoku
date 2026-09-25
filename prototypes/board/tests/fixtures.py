"""One well-posed puzzle, built offline.

A full valid grid from the classic shift pattern, then givens stripped in a
fixed order for as long as the solver still reports exactly one solution.
Deterministic, so every snapshot reads the same board.
"""

from __future__ import annotations

from functools import cache

from board.grid import BOX_SIDE, LINES, SIDE, Cell, Given, Position
from board.solver import solution, solution_count


def rc(row: int, column: int) -> Position:
    return Position(row, column)


def full_grid() -> dict[Position, int]:
    return {
        rc(r, c): (BOX_SIDE * ((r - 1) % BOX_SIDE) + (r - 1) // BOX_SIDE + (c - 1)) % SIDE + 1
        for r in LINES
        for c in LINES
    }


def as_givens(grid: dict[Position, int]) -> frozenset[Cell[Given]]:
    return frozenset(Cell(p, Given(d)) for p, d in grid.items())


@cache
def givens() -> frozenset[Cell[Given]]:
    grid = full_grid()
    kept = dict(grid)
    for pos in sorted(grid):
        trial = {p: d for p, d in kept.items() if p != pos}
        if solution_count(as_givens(trial)) == 1:
            kept = trial
    return as_givens(kept)


@cache
def solved_grid() -> dict[Position, int]:
    return solution(givens())


def solution_at(position: Position) -> int:
    return solved_grid()[position]


def wrong_at(position: Position) -> int:
    return solution_at(position) % SIDE + 1

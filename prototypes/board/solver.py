"""The black boxes sudoku.allium and board.allium name and solver.allium owns.

solution_count is how many complete grids the givens admit, counted only far
enough to tell 0, 1 and "more than one" apart. solution_digit_at reads the one
solution of well-posed givens. Plain backtracking, fewest candidates first.
"""

from __future__ import annotations

from board.grid import DIGITS, GRID, Cell, Given, Position

ENOUGH = 2

Grid = dict[Position, int]

PEERS: dict[Position, tuple[Position, ...]] = {
    p: tuple(q for q in GRID if q.is_peer_of(p)) for p in GRID
}


def _grid_of(givens: frozenset[Cell[Given]]) -> Grid | None:
    """The givens as a grid, or nothing when they can have no solution at all."""
    grid: Grid = {}
    for g in givens:
        if g.position not in PEERS or g.content.digit not in DIGITS or g.position in grid:
            return None
        grid[g.position] = g.content.digit
    for pos, digit in grid.items():
        if any(grid.get(p) == digit for p in PEERS[pos]):
            return None
    return grid


def _candidates(grid: Grid, pos: Position) -> set[int]:
    return set(DIGITS) - {grid[p] for p in PEERS[pos] if p in grid}


def _solutions(grid: Grid, limit: int) -> list[Grid]:
    empty = [p for p in GRID if p not in grid]
    if not empty:
        return [dict(grid)]
    pos = min(empty, key=lambda p: len(_candidates(grid, p)))
    found: list[Grid] = []
    for digit in sorted(_candidates(grid, pos)):
        grid[pos] = digit
        found.extend(_solutions(grid, limit - len(found)))
        del grid[pos]
        if len(found) >= limit:
            break
    return found


def solution_count(givens: frozenset[Cell[Given]]) -> int:
    grid = _grid_of(givens)
    if grid is None:
        return 0
    return len(_solutions(grid, ENOUGH))


def solution(givens: frozenset[Cell[Given]]) -> Grid:
    grid = _grid_of(givens)
    if grid is None:
        msg = "the givens admit no solution"
        raise ValueError(msg)
    found = _solutions(grid, 1)
    if not found:
        msg = "the givens admit no solution"
        raise ValueError(msg)
    return found[0]


def solution_digit_at(givens: frozenset[Cell[Given]], position: Position) -> int:
    return solution(givens)[position]

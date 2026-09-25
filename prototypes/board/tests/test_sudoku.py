"""sudoku.allium's rules: what a setter may pose and what a player may do."""

from __future__ import annotations

import pytest
from inline_snapshot import snapshot

from board.grid import Cell, Given
from board.solver import solution_count
from board.sudoku import Puzzle, RefusalError, Status
from board.tests.fixtures import as_givens, full_grid, givens, rc, solution_at


def test_the_fixture_is_well_posed() -> None:
    assert solution_count(givens()) == 1
    assert len(givens()) == snapshot(29)


def test_set_puzzle_refuses_a_full_grid() -> None:
    with pytest.raises(RefusalError, match=r"givens\.count"):
        Puzzle.set(as_givens(full_grid()))


def test_set_puzzle_refuses_conflicting_givens() -> None:
    grid = full_grid()
    del grid[rc(1, 1)]
    grid[rc(1, 2)] = grid[rc(1, 3)]
    with pytest.raises(RefusalError, match=r"solution_count"):
        Puzzle.set(as_givens(grid))


def test_set_puzzle_refuses_ambiguous_givens() -> None:
    assert solution_count(frozenset()) > 1
    with pytest.raises(RefusalError, match=r"solution_count"):
        Puzzle.set(frozenset())


def test_set_puzzle_refuses_givens_off_the_grid() -> None:
    off = givens() | {Cell(rc(0, 1), Given(1))}
    with pytest.raises(RefusalError, match=r"solution_count"):
        Puzzle.set(off)


def test_a_given_cell_is_no_entry() -> None:
    """A given cell has no move to take: place and erase accept an entry and nothing else.

    mypy holds the rest; here, the entries are the cells that hold no given.
    """
    puzzle = Puzzle.set(givens())
    assert len(puzzle.entries) == len(puzzle.cells) - len(givens())
    assert {cell.position for cell in puzzle.entries}.isdisjoint(g.position for g in givens())


def test_a_cell_that_has_moved_on_is_refused() -> None:
    puzzle = Puzzle.set(givens())
    empty = puzzle.entries[0]
    placed = puzzle.place(empty, 1)
    assert placed != empty
    with pytest.raises(ValueError, match=r"moved on"):
        puzzle.place(empty, 2)
    assert puzzle.at(empty.position) == placed


def test_a_placement_may_conflict_and_an_erasure_needs_a_digit() -> None:
    puzzle = Puzzle.set(givens())
    empty = next(c for c in puzzle.entries if c.row == 2)
    with pytest.raises(RefusalError, match=r"digit\ !=\ null"):
        puzzle.erase(empty)
    clashing = next(p.content.digit for p in puzzle.peers(empty) if p.content.digit is not None)
    placed = puzzle.place(empty, clashing)
    assert puzzle.is_conflicting(placed)
    assert not puzzle.is_consistent
    with pytest.raises(RefusalError, match=r"1\.\.side"):
        puzzle.place(placed, 10)
    erased = puzzle.erase(placed)
    assert erased.content.digit is None
    puzzle.hold_invariants()


def test_solved_is_final() -> None:
    puzzle = Puzzle.set(givens())
    for cell in puzzle.entries:
        puzzle.place(cell, solution_at(cell.position))
    assert puzzle.status is Status.solved
    puzzle.hold_invariants()
    with pytest.raises(RefusalError, match=r"unsolved"):
        puzzle.erase(puzzle.entries[0])

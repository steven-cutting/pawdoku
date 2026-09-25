"""sudoku.allium: the rules, as a puzzle told what to do with its cells.

A Puzzle owns its cells and its status. Its cells are values: a position
holding either a Given, the setter's digit, or an Entry, the player's digit
or nothing. Which of the two a cell holds is its type, so a given cell has
no move to take: `place`, `erase` and `restore` accept an entry and nothing
else, and hand back the cell as it now stands. The black boxes are solver.py's.
"""

from __future__ import annotations

from enum import Enum
from typing import TypeIs

from attrs import define, field

from board.grid import BOX_SIDE, DIGITS, GRID, SIDE, Cell, Entry, Given, Position
from board.solver import solution_count


class RefusalError(Exception):
    """A stimulus one of the rules' `requires` clauses refused."""


def refuse(clause: str, *, unless: bool) -> None:
    if not unless:
        raise RefusalError(clause)


class InvariantError(Exception):
    """A named invariant of a specification that does not hold."""


def hold(name: str, *, when: bool) -> None:
    if not when:
        raise InvariantError(name)


type PuzzleCell = Cell[Given] | Cell[Entry]


def is_entry(cell: PuzzleCell) -> TypeIs[Cell[Entry]]:
    return isinstance(cell.content, Entry)


class Status(Enum):
    unsolved = "unsolved"
    solved = "solved"


@define(eq=False)
class Puzzle:
    """The grid with its givens, and whether it is solved."""

    givens: frozenset[Cell[Given]]
    _status: Status = Status.unsolved
    _cells: dict[Position, PuzzleCell] = field(factory=dict, init=False)

    @classmethod
    def set(cls, givens: frozenset[Cell[Given]]) -> Puzzle:
        """SetPuzzle, then LayOutGrid in the same step."""
        refuse("givens.count < side * side", unless=len(givens) < SIDE * SIDE)
        refuse("solution_count(givens) = 1", unless=solution_count(givens) == 1)
        return cls(givens=givens)

    @classmethod
    def reopen(
        cls, givens: frozenset[Cell[Given]], digits: list[int | None], status: Status
    ) -> Puzzle:
        """The puzzle as a record left it: SetPuzzle's guards, then the digits."""
        puzzle = cls.set(givens)
        for cell, digit in zip(puzzle.cells, digits, strict=True):
            if is_entry(cell):
                puzzle.restore(cell, digit)
            else:
                hold("TheRecordedDigitsKeepTheGivens", when=cell.content.digit == digit)
        hold("TheRecordedStatusIsTheDigits'", when=puzzle.status is status)
        return puzzle

    def __attrs_post_init__(self) -> None:
        """LayOutGrid: a puzzle and its grid come into being together."""
        given_at = {g.position: g for g in self.givens}
        self._cells = {p: given_at.get(p, Cell(p, Entry())) for p in GRID}

    # What can be asked of a puzzle ------------------------------

    @property
    def status(self) -> Status:
        return self._status

    @property
    def cells(self) -> list[PuzzleCell]:
        """Every cell, in grid order."""
        return list(self._cells.values())

    @property
    def entries(self) -> list[Cell[Entry]]:
        """The player's cells: those that hold no given."""
        return [c for c in self.cells if is_entry(c)]

    def at(self, position: Position) -> PuzzleCell:
        return self._cells[position]

    def peers(self, cell: PuzzleCell) -> list[PuzzleCell]:
        """Every other cell that shares a row, a column or a box with this one."""
        return [c for c in self.cells if c.position.is_peer_of(cell.position)]

    def is_conflicting(self, cell: PuzzleCell) -> bool:
        """A conflict is two peers holding one digit; an empty cell conflicts with nothing."""
        digit = cell.content.digit
        return digit is not None and any(p.content.digit == digit for p in self.peers(cell))

    @property
    def filled_cells(self) -> list[PuzzleCell]:
        return [c for c in self.cells if c.content.digit is not None]

    @property
    def conflicting_cells(self) -> list[PuzzleCell]:
        return [c for c in self.cells if self.is_conflicting(c)]

    @property
    def is_full(self) -> bool:
        return len(self.filled_cells) == SIDE * SIDE

    @property
    def is_consistent(self) -> bool:
        return len(self.conflicting_cells) == 0

    @property
    def is_complete(self) -> bool:
        return self.is_full and self.is_consistent

    # PlaceDigit and EraseDigit, each answered with the cell as it now stands

    def place(self, cell: Cell[Entry], digit: int) -> Cell[Entry]:
        self._current(cell)
        refuse("cell.puzzle.status = unsolved", unless=self._status is Status.unsolved)
        refuse("digit in 1..side", unless=digit in DIGITS)
        return self._take(cell.holding(Entry(digit)))

    def erase(self, cell: Cell[Entry]) -> Cell[Entry]:
        self._current(cell)
        refuse("cell.puzzle.status = unsolved", unless=self._status is Status.unsolved)
        refuse("cell.digit != null", unless=cell.content.digit is not None)
        return self._take(cell.holding(Entry()))

    def restore(self, cell: Cell[Entry], digit: int | None) -> Cell[Entry]:
        """Write back a digit a move the rules admitted left here. No rule runs.

        board.allium's Undo and Redo write `puzzle_cell.digit` directly; this
        is the message they send. It is not a move and asks no guard.
        """
        self._current(cell)
        return self._take(cell.holding(Entry(digit)))

    def _current(self, cell: Cell[Entry]) -> None:
        """A cell is a value; only the one the puzzle holds now can be moved on."""
        if self._cells[cell.position] != cell:
            msg = f"{cell.position} has moved on since that cell was read"
            raise ValueError(msg)

    def _take(self, cell: Cell[Entry]) -> Cell[Entry]:
        self._cells[cell.position] = cell
        self.settle()
        return cell

    def settle(self) -> None:
        """PuzzleSolved: fires whenever the puzzle has become complete."""
        if self._status is Status.unsolved and self.is_complete:
            self._status = Status.solved

    # sudoku.allium's invariants, vouched for by the puzzle itself ----

    def hold_invariants(self) -> None:
        cells = self.cells
        hold("TheGridIsWhole", when=len(cells) == SIDE * SIDE)
        hold("OneCellToAPosition", when=len({c.position for c in cells}) == len(cells))
        hold("CellsSitOnTheGrid", when=all(c.position.is_on_the_grid for c in cells))
        hold(
            "CellsSitInTheirBox",
            when=all(
                (c.position.band - 1) * BOX_SIDE < c.row <= c.position.band * BOX_SIDE
                and (c.position.stack - 1) * BOX_SIDE < c.column <= c.position.stack * BOX_SIDE
                for c in cells
            ),
        )
        hold(
            "DigitsAreInRange",
            when=all(c.content.digit is None or c.content.digit in DIGITS for c in cells),
        )
        hold(
            "GivenCellsHoldTheirGiven",
            when=all(c in self.givens for c in cells if not is_entry(c)),
        )
        hold(
            "GivensNeverConflict",
            when=all(
                a.content.digit != b.content.digit
                for a in cells
                if not is_entry(a)
                for b in self.peers(a)
                if not is_entry(b)
            ),
        )
        hold("SolvedMeansComplete", when=self._status is not Status.solved or self.is_complete)

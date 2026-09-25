"""The grid's geometry, the positioned cell, and the payloads the specs name.

A Position is where a cell sits. It knows the box it is in and which other
positions are its peers, so nothing else has to. A Cell is a position with a
payload and nothing more: a value, so a cell never changes. The one thing
that looks like a change, `holding`, is a new cell at the same place with a
new payload, and it is the board's or the puzzle's to swap in.

The payloads sit beside the cell because the cell's methods name them: a
marked cell knows how to take a digit or a mark, a given cell has no such
method to call. Which specification each payload is a construct of is said
on the class.
"""

from __future__ import annotations

from attrs import field, frozen

BOX_SIDE = 3
SIDE = BOX_SIDE * BOX_SIDE
DIGITS = range(1, SIDE + 1)
LINES = range(1, SIDE + 1)


def box_index(line: int) -> int:
    """CellsSitInTheirBox: the one band a row belongs to, or the one stack a column does."""
    return (line - 1) // BOX_SIDE + 1


@frozen(order=True)
class Position:
    """Where a cell sits: rows from the top and columns from the left, both from 1."""

    row: int
    column: int

    @property
    def band(self) -> int:
        return box_index(self.row)

    @property
    def stack(self) -> int:
        return box_index(self.column)

    @property
    def ordinal(self) -> int:
        """The position's place in grid order, from 0."""
        return (self.row - 1) * SIDE + (self.column - 1)

    @property
    def is_on_the_grid(self) -> bool:
        return self.row in LINES and self.column in LINES

    def is_peer_of(self, other: Position) -> bool:
        """Shares a row, a column or a box with this one, and is not this one."""
        return self != other and (
            self.row == other.row
            or self.column == other.column
            or (self.band == other.band and self.stack == other.stack)
        )

    def __str__(self) -> str:
        return f"r{self.row}c{self.column}"


# Every position from row 1, column 1 to row side, column side, each once.
GRID: tuple[Position, ...] = tuple(Position(r, c) for r in LINES for c in LINES)


@frozen
class Given:
    """sudoku.allium's Given: the setter's digit, never the player's to change."""

    digit: int


@frozen
class Entry:
    """sudoku.allium's Cell as the player holds it: a digit, or nothing while it is empty."""

    digit: int | None = None


@frozen
class Marked:
    """board.allium's BoardCell as the player holds it: the entry, and the note beside or beneath it."""

    entry: Entry = field(factory=Entry)
    note: frozenset[int] = frozenset()

    @property
    def digit(self) -> int | None:
        return self.entry.digit

    @property
    def holds_players_digit(self) -> bool:
        return self.digit is not None

    @property
    def accepts_marks(self) -> bool:
        return self.digit is None

    @property
    def shows_note(self) -> bool:
        return self.digit is None

    def with_digit(self, digit: int | None) -> Marked:
        return Marked(Entry(digit), self.note)

    def with_mark(self, digit: int) -> Marked:
        return Marked(self.entry, self.note | {digit})

    def without_mark(self, digit: int) -> Marked:
        return Marked(self.entry, self.note - {digit})


@frozen
class Cell[T]:
    """A payload at a position. What the payload is decides what the cell is for.

    The methods below are typed on `self`, so only a marked cell has them:
    mypy refuses `with_mark` on a `Cell[Given]` as it would refuse a missing
    attribute.
    """

    position: Position
    content: T

    @property
    def row(self) -> int:
        return self.position.row

    @property
    def column(self) -> int:
        return self.position.column

    def holding[U](self, content: U) -> Cell[U]:
        """The same place with a new payload: how a cell that never changes is replaced."""
        return Cell(self.position, content)

    @property
    def puzzle_cell(self: Cell[Marked]) -> Cell[Entry]:
        """The spec's BoardCell.puzzle_cell: the same place as the puzzle holds it."""
        return self.holding(self.content.entry)

    def with_digit(self: Cell[Marked], digit: int | None) -> Cell[Marked]:
        return self.holding(self.content.with_digit(digit))

    def with_mark(self: Cell[Marked], digit: int) -> Cell[Marked]:
        return self.holding(self.content.with_mark(digit))

    def without_mark(self: Cell[Marked], digit: int) -> Cell[Marked]:
        return self.holding(self.content.without_mark(digit))

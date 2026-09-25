"""board.allium: a puzzle in play, as a board told what to do with its cells.

A Board is sent the player's stimuli with the cell they are about: place,
erase, write_mark, strike_mark, check; and undo and redo on its own. Its
cells are values: a position holding either the setter's Given or a Marked
payload, the player's entry with a note. Which of the two is the cell's
type, so no rule can be sent a given: the rules accept a marked cell and
nothing else, and hand back the cell as it now stands. A Move is an object
that knows how to take itself back and do itself again, one class per kind.
Readings, the record and the text rendering are answers the board gives.
"""

from __future__ import annotations

from typing import Any, ClassVar, TypeIs

from attrs import define, field, frozen

from board.grid import BOX_SIDE, DIGITS, SIDE, Cell, Entry, Given, Marked, Position
from board.solver import solution_digit_at
from board.sudoku import Puzzle, RefusalError, Status, hold, is_entry, refuse

Record = dict[str, Any]


type BoardCell = Cell[Given] | Cell[Marked]


def is_marked(cell: BoardCell) -> TypeIs[Cell[Marked]]:
    return isinstance(cell.content, Marked)


def note_of(cell: BoardCell) -> frozenset[int]:
    return cell.content.note if is_marked(cell) else frozenset()


@frozen
class Reading:
    """The board as it stood once one move and no later one had been made."""

    cells: tuple[BoardCell, ...]

    def at(self, position: Position) -> BoardCell:
        return self.cells[position.ordinal]

    def marked_at(self, position: Position) -> Cell[Marked]:
        cell = self.at(position)
        if not is_marked(cell):
            msg = f"{position} holds a given, which no move or check is about"
            raise ValueError(msg)
        return cell

    def digit_at(self, cell: BoardCell) -> int | None:
        return self.at(cell.position).content.digit

    def note_at(self, cell: BoardCell) -> frozenset[int]:
        return note_of(self.at(cell.position))

    def write(self) -> Record:
        return {
            "digits": [c.content.digit for c in self.cells],
            "notes": [sorted(note_of(c)) for c in self.cells],
        }

    @classmethod
    def opening(cls, cells: list[BoardCell]) -> Reading:
        """The reading before any move: the givens, and every entry empty and unmarked."""
        return cls(tuple(c.holding(Marked()) if is_marked(c) else c for c in cells))

    @classmethod
    def reopen(cls, cells: list[BoardCell], record: Record) -> Reading:
        return cls(
            tuple(
                c.holding(Marked(Entry(digit), frozenset(note))) if is_marked(c) else c
                for c, digit, note in zip(cells, record["digits"], record["notes"], strict=True)
            )
        )


@define(eq=False)
class Move:
    """One thing the player did, able to take itself back and do itself again.

    The target and the struck peers are kept as they stood before the move,
    so taking it back is putting them back. Undo only ever reaches the latest
    standing move, so what stood before it is exactly what stands after.
    """

    kind: ClassVar[str]

    _board: Board
    index: int
    target: Cell[Marked]
    digit: int | None
    struck_from: frozenset[Cell[Marked]]
    _after: Reading
    _is_undone: bool = False

    @property
    def is_undone(self) -> bool:
        return self._is_undone

    @property
    def is_latest_standing(self) -> bool:
        return not self._is_undone and all(
            m.index <= self.index for m in self._board.standing_moves
        )

    @property
    def is_next_to_redo(self) -> bool:
        return self._is_undone and all(m.index >= self.index for m in self._board.undone_moves)

    @property
    def digit_before(self) -> int | None:
        raise NotImplementedError

    @property
    def reading(self) -> Reading:
        return self._after

    def digit_after(self, cell: BoardCell) -> int | None:
        return self._after.digit_at(cell)

    def note_after(self, cell: BoardCell) -> frozenset[int]:
        return self._after.note_at(cell)

    def take_back(self) -> None:
        self._is_undone = True
        for cell in (self.target, *self.struck_from):
            self._board.restore(cell)

    def retake(self) -> None:
        self._is_undone = False
        self._forward()

    def _forward(self) -> None:
        raise NotImplementedError

    def _digit(self) -> int:
        if self.digit is None:
            msg = f"move {self.index} of kind {self.kind} carries no digit"
            raise ValueError(msg)
        return self.digit

    def carries_what_its_kind_needs(self) -> bool:
        raise NotImplementedError

    def describe(self) -> str:
        raise NotImplementedError

    def render(self) -> str:
        return f"- {'~' if self._is_undone else ''}{self.index} {self.kind} {self.describe()}"

    def write(self) -> Record:
        return {
            "index": self.index,
            "kind": self.kind,
            "target": [self.target.row, self.target.column],
            "digit": self.digit,
            "digit_before": self.digit_before,
            "struck_from": sorted([c.row, c.column] for c in self.struck_from),
            "is_undone": self._is_undone,
            "after": self._after.write(),
        }

    @staticmethod
    def reopen(board: Board, record: Record, before: Reading) -> Move:
        """The move again, its target and struck peers read off the reading before it."""
        kind = next(k for k in KINDS if k.kind == record["kind"])
        move = kind(
            board=board,
            index=record["index"],
            target=before.marked_at(Position(*record["target"])),
            digit=record["digit"],
            struck_from=frozenset(
                before.marked_at(Position(r, c)) for r, c in record["struck_from"]
            ),
            after=Reading.reopen(board.cells, record["after"]),
            is_undone=record["is_undone"],
        )
        hold(
            "TheRecordedDigitBeforeIsTheTarget's", when=move.digit_before == record["digit_before"]
        )
        return move


class Placement(Move):
    kind = "place"

    @property
    def digit_before(self) -> int | None:
        return self.target.content.digit

    def _forward(self) -> None:
        self._board.restore(self.target.with_digit(self._digit()))
        for peer in self.struck_from:
            self._board.restore(peer.without_mark(self._digit()))

    def carries_what_its_kind_needs(self) -> bool:
        return self.digit is not None

    def describe(self) -> str:
        was = "-" if self.digit_before is None else str(self.digit_before)
        struck = " ".join(
            str(c.position) for c in sorted(self.struck_from, key=lambda c: c.position)
        )
        text = f"{self.target.position}={self.digit} (was {was})"
        return text + (f" struck {struck}" if struck else "")


class Erasure(Move):
    kind = "erase"

    @property
    def digit_before(self) -> int | None:
        return self.target.content.digit

    def _forward(self) -> None:
        self._board.restore(self.target.with_digit(None))

    def carries_what_its_kind_needs(self) -> bool:
        return self.digit is None and self.digit_before is not None

    def describe(self) -> str:
        return f"{self.target.position} (was {self.digit_before})"


class MarkMove(Move):
    @property
    def digit_before(self) -> int | None:
        return None

    def carries_what_its_kind_needs(self) -> bool:
        return self.digit is not None and not self.struck_from


class WrittenMark(MarkMove):
    kind = "write_mark"

    def _forward(self) -> None:
        self._board.restore(self.target.with_mark(self._digit()))

    def describe(self) -> str:
        return f"{self.target.position}+{self.digit}"


class StruckMark(MarkMove):
    kind = "strike_mark"

    def _forward(self) -> None:
        self._board.restore(self.target.without_mark(self._digit()))

    def describe(self) -> str:
        return f"{self.target.position}-{self.digit}"


KINDS: tuple[type[Move], ...] = (Placement, Erasure, WrittenMark, StruckMark)


@frozen
class Check:
    """One question asked and answered: never a move, never taken back.

    The target is the board's cell, live: the digit is what the question was
    about, as it stood, and the cell may since have changed.
    """

    _board: Board
    index: int
    after_move: int
    position: Position
    digit: int
    is_right: bool

    @property
    def target(self) -> Cell[Marked]:
        return self._board.entry_at(self.position)

    def render(self) -> str:
        verdict = "right" if self.is_right else "wrong"
        return (
            f"- {self.index} after move {self.after_move}: {self.position}={self.digit} {verdict}"
        )

    def write(self) -> Record:
        return {
            "index": self.index,
            "after_move": self.after_move,
            "target": [self.position.row, self.position.column],
            "digit": self.digit,
            "is_right": self.is_right,
        }

    @classmethod
    def reopen(cls, board: Board, record: Record) -> Check:
        return cls(
            board=board,
            index=record["index"],
            after_move=record["after_move"],
            position=Position(*record["target"]),
            digit=record["digit"],
            is_right=record["is_right"],
        )


@define(eq=False)
class Board:
    """The puzzle in play, with its notes, its moves and its checks."""

    _puzzle: Puzzle
    _reopened_from: Record | None = None
    _cells: dict[Position, BoardCell] = field(factory=dict, init=False)
    _moves: list[Move] = field(factory=list, init=False)
    _checks: list[Check] = field(factory=list, init=False)

    # Opening ---------------------------------------------------

    @classmethod
    def open(cls, givens: frozenset[Cell[Given]]) -> Board:
        """SetPuzzle, then OpenBoard and LayOutBoard in the same step."""
        return cls(puzzle=Puzzle.set(givens))

    def __attrs_post_init__(self) -> None:
        """LayOutBoard: one cell of the board for each cell of the grid.

        Given a record, the notes, moves and checks it holds come back too.
        """
        self._cells = {
            c.position: c.holding(Marked(c.content)) if is_entry(c) else c
            for c in self._puzzle.cells
        }
        if self._reopened_from is not None:
            record, self._reopened_from = self._reopened_from, None
            before = Reading.opening(self.cells)
            self._cells = {c.position: c for c in Reading.reopen(self.cells, record).cells}
            for m in record["moves"]:
                move = Move.reopen(self, m, before)
                self._moves.append(move)
                before = move.reading
            self._checks = [Check.reopen(self, c) for c in record["checks"]]

    # What Playing exposes ----------------------------------------

    @property
    def status(self) -> Status:
        return self._puzzle.status

    @property
    def is_full(self) -> bool:
        return self._puzzle.is_full

    @property
    def is_consistent(self) -> bool:
        return self._puzzle.is_consistent

    @property
    def givens(self) -> frozenset[Cell[Given]]:
        return self._puzzle.givens

    @property
    def cells(self) -> list[BoardCell]:
        """Every cell, in grid order."""
        return list(self._cells.values())

    @property
    def marked(self) -> list[Cell[Marked]]:
        """The player's cells: those that hold no given."""
        return [c for c in self.cells if is_marked(c)]

    def at(self, position: Position) -> BoardCell:
        return self._cells[position]

    def entry_at(self, position: Position) -> Cell[Marked]:
        """The player's cell there. The one place a given is refused at run time.

        Playing offers a move only on a cell that is not given; past this
        boundary the rules take a marked cell and the type checker keeps a
        given out of them.
        """
        cell = self.at(position)
        if not is_marked(cell):
            clause = "not target.puzzle_cell.is_given"
            raise RefusalError(clause)
        return cell

    def entry(self, row: int, column: int) -> Cell[Marked]:
        """The coordinate boundary: where a row and a column become a cell."""
        return self.entry_at(Position(row, column))

    def is_conflicting(self, cell: BoardCell) -> bool:
        return self._puzzle.is_conflicting(self._puzzle.at(cell.position))

    @property
    def moves(self) -> list[Move]:
        return list(self._moves)

    @property
    def checks(self) -> list[Check]:
        return list(self._checks)

    @property
    def standing_moves(self) -> list[Move]:
        return [m for m in self._moves if not m.is_undone]

    @property
    def undone_moves(self) -> list[Move]:
        return [m for m in self._moves if m.is_undone]

    @property
    def latest_standing_moves(self) -> list[Move]:
        return [m for m in self._moves if m.is_latest_standing]

    @property
    def next_to_redo(self) -> list[Move]:
        return [m for m in self._moves if m.is_next_to_redo]

    @property
    def can_undo(self) -> bool:
        return self.status is Status.unsolved and len(self.standing_moves) > 0

    @property
    def can_redo(self) -> bool:
        return self.status is Status.unsolved and len(self.undone_moves) > 0

    def after(self, index: int) -> Move:
        """The move at this index, standing or undone, for reading back."""
        return next(m for m in self._moves if m.index == index)

    def reading(self) -> Reading:
        return Reading(tuple(self.cells))

    # Swapping cells ----------------------------------------------

    def _current(self, cell: Cell[Marked]) -> None:
        """A cell is a value; only the one the board holds now can be moved on."""
        if self._cells[cell.position] != cell:
            msg = f"{cell.position} has moved on since that cell was read"
            raise ValueError(msg)

    def _take(self, cell: Cell[Marked]) -> Cell[Marked]:
        self._cells[cell.position] = cell
        return cell

    def restore(self, cell: Cell[Marked]) -> Cell[Marked]:
        """Put a cell back or forward as a move says: the direct write, no rule runs."""
        self._puzzle.restore(self.entry_at(cell.position).puzzle_cell, cell.content.digit)
        return self._take(cell)

    # Moves -----------------------------------------------------

    def _unsolved(self) -> None:
        refuse("board.puzzle.status = unsolved", unless=self.status is Status.unsolved)

    def _record(
        self,
        kind: type[Move],
        target: Cell[Marked],
        digit: int | None,
        struck_from: frozenset[Cell[Marked]] = frozenset(),
    ) -> None:
        """Every move discards whatever was undone and takes the next index."""
        self._moves = self.standing_moves
        self._moves.append(
            kind(
                board=self,
                index=len(self._moves) + 1,
                target=target,
                digit=digit,
                struck_from=struck_from,
                after=self.reading(),
            )
        )

    def place(self, target: Cell[Marked], digit: int) -> Cell[Marked]:
        self._current(target)
        self._unsolved()
        refuse("digit in 1..side", unless=digit in DIGITS)
        struck = frozenset(
            c
            for c in self.marked
            if c.position.is_peer_of(target.position) and digit in c.content.note
        )
        for peer in struck:
            self._take(peer.without_mark(digit))
        entry = self._puzzle.place(target.puzzle_cell, digit)
        placed = self._take(target.with_digit(entry.content.digit))
        self._record(Placement, target, digit, struck)
        return placed

    def erase(self, target: Cell[Marked]) -> Cell[Marked]:
        self._current(target)
        self._unsolved()
        refuse("target.holds_players_digit", unless=target.content.holds_players_digit)
        entry = self._puzzle.erase(target.puzzle_cell)
        erased = self._take(target.with_digit(entry.content.digit))
        self._record(Erasure, target, None)
        return erased

    def write_mark(self, target: Cell[Marked], digit: int) -> Cell[Marked]:
        self._current(target)
        self._unsolved()
        refuse("target.accepts_marks", unless=target.content.accepts_marks)
        refuse("digit in 1..side", unless=digit in DIGITS)
        refuse("digit not in target.note", unless=digit not in target.content.note)
        written = self._take(target.with_mark(digit))
        self._record(WrittenMark, target, digit)
        return written

    def strike_mark(self, target: Cell[Marked], digit: int) -> Cell[Marked]:
        self._current(target)
        self._unsolved()
        refuse("target.accepts_marks", unless=target.content.accepts_marks)
        refuse("digit in target.note", unless=digit in target.content.note)
        struck = self._take(target.without_mark(digit))
        self._record(StruckMark, target, digit)
        return struck

    # Taking back and re-taking --------------------------------

    def undo(self) -> None:
        refuse("board.can_undo", unless=self.can_undo)
        for move in self.latest_standing_moves:
            move.take_back()

    def redo(self) -> None:
        refuse("board.can_redo", unless=self.can_redo)
        for move in self.next_to_redo:
            move.retake()

    # The check -------------------------------------------------

    def check(self, target: Cell[Marked]) -> Check:
        self._current(target)
        self._unsolved()
        refuse("target.holds_players_digit", unless=target.content.holds_players_digit)
        digit = target.content.digit
        if digit is None:  # pragma: no cover - holds_players_digit already says so
            raise AssertionError
        check = Check(
            board=self,
            index=len(self._checks) + 1,
            after_move=len(self.standing_moves),
            position=target.position,
            digit=digit,
            is_right=digit == solution_digit_at(self.givens, target.position),
        )
        self._checks.append(check)
        return check

    # Recording -------------------------------------------------

    def write(self) -> Record:
        """The board written down whole: JSON-plain, nothing of where it is kept."""
        return {
            "givens": sorted([g.row, g.column, g.content.digit] for g in self.givens),
            "status": self.status.value,
            **self.reading().write(),
            "moves": [m.write() for m in self._moves],
            "checks": [c.write() for c in self._checks],
        }

    @classmethod
    def reopen(cls, record: Record) -> Board:
        """The same board again. Nothing but the record is consulted."""
        givens = frozenset(Cell(Position(r, c), Given(d)) for r, c, d in record["givens"])
        puzzle = Puzzle.reopen(givens, record["digits"], Status(record["status"]))
        return cls(puzzle=puzzle, reopened_from=record)

    # Rendering -------------------------------------------------

    def render(self) -> str:
        """The board as text: the grid, non-empty notes, moves and checks.

        Cells are four characters: `[5] ` a given, ` 5  ` the player's digit,
        ` .  ` empty, and a trailing `!` where the cell conflicts. Hidden
        notes are marked; undone moves are prefixed `~`. No line starts
        with a space, so a snapshot of the text sits inside a test file
        without upsetting its indentation rules.
        """
        yes = {True: "yes", False: "no"}
        lines = [
            (
                f"status: {self.status.value}  full: {yes[self.is_full]}  "
                f"consistent: {yes[self.is_consistent]}  "
                f"undo: {yes[self.can_undo]}  redo: {yes[self.can_redo]}"
            ),
            *self._render_grid(),
            "notes:",
            *self._render_notes(),
            "moves:",
            *([m.render() for m in self._moves] or ["(none)"]),
            "checks:",
            *([c.render() for c in self._checks] or ["(none)"]),
        ]
        return "\n".join(lines) + "\n"

    def _render_grid(self) -> list[str]:
        lines: list[str] = []
        cells = self.cells
        for row in range(1, SIDE + 1):
            if row > 1 and (row - 1) % BOX_SIDE == 0:
                lines.append("---" + "+".join(["-" * (4 * BOX_SIDE + 1)] * BOX_SIDE))
            rendered = [
                self._render_cell(c, conflicting=self.is_conflicting(c))
                for c in cells[(row - 1) * SIDE : row * SIDE]
            ]
            boxes = [
                " " + "".join(rendered[b * BOX_SIDE : (b + 1) * BOX_SIDE]) for b in range(BOX_SIDE)
            ]
            lines.append((f"r{row} " + "|".join(boxes)).rstrip())
        return lines

    @staticmethod
    def _render_cell(cell: BoardCell, *, conflicting: bool) -> str:
        if cell.content.digit is None:
            body = " . "
        elif is_marked(cell):
            body = f" {cell.content.digit} "
        else:
            body = f"[{cell.content.digit}]"
        return body + ("!" if conflicting else " ")

    def _render_notes(self) -> list[str]:
        lines = [
            f"- {c.position}: {' '.join(str(d) for d in sorted(c.content.note))}"
            + ("" if c.content.shows_note else " (beneath a digit)")
            for c in self.marked
            if c.content.note
        ]
        return lines or ["(none)"]

    # Invariants ------------------------------------------------

    def hold_invariants(self) -> None:
        """Every named invariant of board.allium, and the puzzle's own.

        Two are facts of the types and have no run-time check to make:
        MovesNeverTouchAGiven and NoMarkInAGiven, because a move takes a
        marked cell and only a marked cell has a note. A check's target is
        held here, because a record supplies it. The last check is the
        model's own: the board's cells mirror the puzzle's.
        """
        self._puzzle.hold_invariants()
        cells, moves, checks = self.cells, self._moves, self._checks
        hold("TheBoardIsWhole", when=len(cells) == SIDE * SIDE)
        hold("OneBoardCellToAPosition", when=len({c.position for c in cells}) == len(cells))
        hold("MarksAreDigits", when=all(d in DIGITS for c in self.marked for d in c.content.note))
        hold("MoveIndicesRunFromOne", when=all(1 <= m.index <= len(moves) for m in moves))
        hold("MoveIndicesAreDistinct", when=len({m.index for m in moves}) == len(moves))
        hold(
            "MovesCarryWhatTheirKindNeeds",
            when=all(m.carries_what_its_kind_needs() for m in moves),
        )
        hold(
            "UndoneMovesAreTheLatest",
            when=all(
                all(o.index < m.index or o.is_undone for o in moves) for m in moves if m.is_undone
            ),
        )
        standing = len(self.standing_moves)
        hold(
            "WhatIsReTakenComesNext",
            when=all(m.index == standing + 1 for m in moves if m.is_next_to_redo),
        )
        hold(
            "ASolvedBoardHasNothingUndone",
            when=self.status is not Status.solved or not self.undone_moves,
        )
        hold(
            "UpkeepStrikesPeersOfAPlacement",
            when=all(
                p.position.is_peer_of(m.target.position) for m in moves for p in m.struck_from
            ),
        )
        hold(
            "TheMovesReplayToTheBoard",
            when=all(
                m.digit_after(c) == c.content.digit and m.note_after(c) == note_of(c)
                for m in moves
                if m.is_latest_standing
                for c in cells
            ),
        )
        hold("ChecksRunFromOne", when=all(1 <= c.index <= len(checks) for c in checks))
        hold("CheckIndicesAreDistinct", when=len({c.index for c in checks}) == len(checks))
        hold("ACheckIsOnAPlayersCell", when=all(is_marked(self.at(c.position)) for c in checks))
        hold(
            "TheBoardMirrorsItsPuzzle",
            when=all(
                (c.puzzle_cell if is_marked(c) else c) == self._puzzle.at(c.position)
                for c in cells
            ),
        )

    def plays(self, puzzle: Puzzle) -> bool:
        return self._puzzle is puzzle

    def shares_a_puzzle_with(self, other: Board) -> bool:
        return other.plays(self._puzzle)


def hold_invariants(*boards: Board) -> None:
    """Every board's own invariants, and the one that spans boards."""
    for board in boards:
        board.hold_invariants()
    hold(
        "OneBoardToAPuzzle",
        when=not any(a.shares_a_puzzle_with(b) for a in boards for b in boards if a is not b),
    )

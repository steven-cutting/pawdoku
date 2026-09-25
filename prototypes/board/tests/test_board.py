"""board.allium's Playing surface, one scenario per guarantee.

Each scenario snapshots the rendering after the stimuli that matter, and
holds every invariant after every step. Read the renderings: they are the
review.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from inline_snapshot import snapshot

from board.board import Board, is_marked
from board.sudoku import RefusalError
from board.tests.fixtures import givens, rc, solution_at, wrong_at

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture
def board() -> Board:
    return Board.open(givens())


def step(board: Board, act: Callable[[], object]) -> str:
    act()
    board.hold_invariants()
    return board.render()


def grid_and_notes(rendering: str) -> str:
    """The rendering without its status line and its move and check lists."""
    return rendering.partition("\n")[2].partition("moves:")[0]


def test_the_board_opens_as_the_puzzle_is(board: Board) -> None:
    board.hold_invariants()
    assert board.render() == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: no  redo: no
r1   .   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
(none)
moves:
(none)
checks:
(none)
""")


def test_every_move_is_the_boards_and_a_refused_move_is_not_recorded(board: Board) -> None:
    given = next(c for c in board.cells if not is_marked(c))
    empty = next(c for c in board.marked if c.content.accepts_marks)
    with pytest.raises(RefusalError, match=r"is_given"):
        board.entry(given.row, given.column)
    with pytest.raises(RefusalError, match=r"1\.\.side"):
        board.place(empty, 0)
    with pytest.raises(RefusalError, match=r"holds_players_digit"):
        board.erase(empty)
    with pytest.raises(RefusalError, match=r"digit\ in\ target\.note"):
        board.strike_mark(empty, 5)
    board.hold_invariants()
    assert board.moves == []


def test_upkeep_strikes_the_placed_digit_from_every_peers_note(board: Board) -> None:
    peers, not_a_peer = [rc(1, 9), rc(9, 1), rc(2, 2)], rc(5, 5)
    assert all(board.entry_at(p).content.accepts_marks for p in [rc(1, 1), *peers, not_a_peer])
    for position in [*peers, not_a_peer]:
        cell = board.write_mark(board.entry_at(position), 7)
        board.write_mark(cell, 8)
    c11 = board.write_mark(board.entry(1, 1), 7)
    assert step(board, lambda: board.place(c11, 7)) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   7   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 7 (beneath a digit)
- r1c9: 8
- r2c2: 8
- r5c5: 7 8
- r9c1: 8
moves:
- 1 write_mark r1c9+7
- 2 write_mark r1c9+8
- 3 write_mark r9c1+7
- 4 write_mark r9c1+8
- 5 write_mark r2c2+7
- 6 write_mark r2c2+8
- 7 write_mark r5c5+7
- 8 write_mark r5c5+8
- 9 write_mark r1c1+7
- 10 place r1c1=7 (was -) struck r1c9 r2c2 r9c1
checks:
(none)
""")


def test_undo_and_redo_are_exact(board: Board) -> None:
    board.write_mark(board.entry(1, 2), 3)
    c11 = board.write_mark(board.entry(1, 1), 3)
    before = step(board, lambda: board.write_mark(c11, 4))
    after = step(board, lambda: board.place(board.entry(1, 1), 3))
    assert after == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   3   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 3 4 (beneath a digit)
moves:
- 1 write_mark r1c2+3
- 2 write_mark r1c1+3
- 3 write_mark r1c1+4
- 4 place r1c1=3 (was -) struck r1c2
checks:
(none)
""")
    undone = step(board, board.undo)
    assert undone == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: yes
r1   .   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 3 4
- r1c2: 3
moves:
- 1 write_mark r1c2+3
- 2 write_mark r1c1+3
- 3 write_mark r1c1+4
- ~4 place r1c1=3 (was -) struck r1c2
checks:
(none)
""")
    assert grid_and_notes(undone) == grid_and_notes(before)
    assert undone.splitlines()[0] == before.splitlines()[0].replace("redo: no", "redo: yes")
    assert step(board, board.redo) == after


def test_erasing_gives_the_peers_nothing_back(board: Board) -> None:
    board.write_mark(board.entry(1, 2), 5)
    c11 = board.place(board.entry(1, 1), 5)
    assert step(board, lambda: board.erase(c11)) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   .   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
(none)
moves:
- 1 write_mark r1c2+5
- 2 place r1c1=5 (was -) struck r1c2
- 3 erase r1c1 (was 5)
checks:
(none)
""")


def test_a_new_move_discards_what_was_undone(board: Board) -> None:
    board.place(board.entry(1, 1), 1)
    board.place(board.entry(1, 2), 2)
    board.undo()
    board.undo()
    assert step(board, lambda: board.write_mark(board.entry(1, 1), 9)) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   .   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 9
moves:
- 1 write_mark r1c1+9
checks:
(none)
""")
    assert not board.can_redo
    with pytest.raises(RefusalError, match=r"can_redo"):
        board.redo()


def test_a_mark_is_a_move(board: Board) -> None:
    c11 = board.write_mark(board.entry(1, 1), 2)
    board.strike_mark(c11, 2)
    board.undo()
    assert step(board, board.undo) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: no  redo: yes
r1   .   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
(none)
moves:
- ~1 write_mark r1c1+2
- ~2 strike_mark r1c1-2
checks:
(none)
""")
    board.redo()
    assert step(board, board.redo) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   .   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
(none)
moves:
- 1 write_mark r1c1+2
- 2 strike_mark r1c1-2
checks:
(none)
""")


def test_undo_stops_with_the_puzzle(board: Board) -> None:
    for cell in board.marked:
        board.place(cell, solution_at(cell.position))
    board.hold_invariants()
    assert board.render().splitlines()[0] == snapshot(
        "status: solved  full: yes  consistent: yes  undo: no  redo: no"
    )
    assert not board.can_undo
    with pytest.raises(RefusalError, match=r"can_undo"):
        board.undo()
    with pytest.raises(RefusalError, match=r"can_redo"):
        board.redo()


def test_every_past_board_is_readable(board: Board) -> None:
    c11 = board.place(board.entry(1, 1), 1)
    c12 = board.write_mark(board.entry(1, 2), 1)
    board.erase(c11)
    board.undo()
    readings = [
        (m.index, m.is_undone, m.digit_after(c11), sorted(m.note_after(c12))) for m in board.moves
    ]
    assert readings == snapshot([(1, False, 1, []), (2, False, 1, [1]), (3, True, None, [1])])
    assert board.after(2).digit_after(c11) == 1
    board.hold_invariants()
    assert board.can_redo


def test_givens_never_move(board: Board) -> None:
    """No rule can be sent a given: each takes a marked cell, which mypy holds.

    What is left to run time is the boundary where a position becomes a
    cell, and it refuses a given's position.
    """
    given = next(c for c in board.cells if not is_marked(c))
    with pytest.raises(RefusalError, match=r"is_given"):
        board.entry(given.row, given.column)
    with pytest.raises(RefusalError, match=r"is_given"):
        board.entry_at(given.position)
    assert board.moves == []
    assert board.checks == []


def test_a_cell_that_has_moved_on_is_refused(board: Board) -> None:
    c11 = board.entry(1, 1)
    marked = board.write_mark(c11, 1)
    with pytest.raises(ValueError, match=r"moved on"):
        board.place(c11, 1)
    assert board.at(rc(1, 1)) == marked
    assert len(board.moves) == 1


def test_a_note_waits_beneath_a_digit(board: Board) -> None:
    c11 = board.write_mark(board.entry(1, 1), 4)
    c11 = board.write_mark(c11, 6)
    assert step(board, lambda: board.place(c11, 5)) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   5   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 4 6 (beneath a digit)
moves:
- 1 write_mark r1c1+4
- 2 write_mark r1c1+6
- 3 place r1c1=5 (was -)
checks:
(none)
""")
    with pytest.raises(RefusalError, match=r"accepts_marks"):
        board.write_mark(board.entry(1, 1), 7)
    assert step(board, lambda: board.place(board.entry(2, 1), 6)) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   5   .   .  |  .   .   .  |  .   .   .
r2   6   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 4 (beneath a digit)
moves:
- 1 write_mark r1c1+4
- 2 write_mark r1c1+6
- 3 place r1c1=5 (was -)
- 4 place r2c1=6 (was -) struck r1c1
checks:
(none)
""")
    assert step(board, board.undo) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: yes
r1   5   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 4 6 (beneath a digit)
moves:
- 1 write_mark r1c1+4
- 2 write_mark r1c1+6
- 3 place r1c1=5 (was -)
- ~4 place r2c1=6 (was -) struck r1c1
checks:
(none)
""")
    board.redo()
    assert step(board, lambda: board.erase(board.entry(1, 1))) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   .   .   .  |  .   .   .  |  .   .   .
r2   6   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
- r1c1: 4
moves:
- 1 write_mark r1c1+4
- 2 write_mark r1c1+6
- 3 place r1c1=5 (was -)
- 4 place r2c1=6 (was -) struck r1c1
- 5 erase r1c1 (was 5)
checks:
(none)
""")


def test_every_check_is_kept_and_never_tells_the_digit(board: Board) -> None:
    board.check(board.place(board.entry(1, 1), wrong_at(rc(1, 1))))
    board.check(board.place(board.entry(1, 2), solution_at(rc(1, 2))))
    board.undo()
    board.undo()
    c11 = board.place(board.entry(1, 1), solution_at(rc(1, 1)))
    assert step(board, lambda: board.check(c11)) == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   1   .   .  |  .   .   .  |  .   .   .
r2   .   .   .  |  .   .   .  | [1] [2] [3]
r3   .   .   .  | [1] [2] [3] | [4] [5] [6]
----------------+-------------+-------------
r4   .   .   .  |  .   .   .  |  .   .   .
r5   .   .   .  |  .   .   .  | [2] [3] [4]
r6   .   .  [1] | [2] [3]  .  | [5] [6] [7]
----------------+-------------+-------------
r7   .   .  [5] |  .  [7] [8] |  .   .   .
r8   .  [7] [8] |  .   .   .  | [3]  .   .
r9   .  [1] [2] | [3] [4]  .  | [6]  .   .
notes:
(none)
moves:
- 1 place r1c1=1 (was -)
checks:
- 1 after move 1: r1c1=2 wrong
- 2 after move 2: r1c2=2 right
- 3 after move 1: r1c1=1 right
""")
    assert [type(c.is_right) for c in board.checks] == [bool, bool, bool]
    with pytest.raises(RefusalError, match=r"holds_players_digit"):
        board.check(board.entry(1, 2))

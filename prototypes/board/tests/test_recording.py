"""The Recording contract: a board written down and had again."""

from __future__ import annotations

from inline_snapshot import snapshot

from board.board import Board, hold_invariants
from board.tests.fixtures import givens, rc, solution_at, wrong_at


def played() -> Board:
    board = Board.open(givens())
    board.write_mark(board.entry(1, 2), 3)
    c11 = board.write_mark(board.entry(1, 1), 3)
    board.place(c11, 3)
    c21 = board.place(board.entry(2, 1), wrong_at(rc(2, 1)))
    board.check(c21)
    c21 = board.erase(c21)
    board.place(c21, solution_at(rc(2, 1)))
    board.undo()
    return board


def test_the_record_is_plain_data() -> None:
    record = played().write()
    moves = [{k: v for k, v in m.items() if k != "after"} for m in record["moves"]]
    assert all(len(m["after"]["digits"]) == 81 for m in record["moves"])
    assert {
        "givens": record["givens"],
        "status": record["status"],
        "moves": moves,
        "checks": record["checks"],
    } == snapshot(
        {
            "givens": [
                [2, 7, 1],
                [2, 8, 2],
                [2, 9, 3],
                [3, 4, 1],
                [3, 5, 2],
                [3, 6, 3],
                [3, 7, 4],
                [3, 8, 5],
                [3, 9, 6],
                [5, 7, 2],
                [5, 8, 3],
                [5, 9, 4],
                [6, 3, 1],
                [6, 4, 2],
                [6, 5, 3],
                [6, 7, 5],
                [6, 8, 6],
                [6, 9, 7],
                [7, 3, 5],
                [7, 5, 7],
                [7, 6, 8],
                [8, 2, 7],
                [8, 3, 8],
                [8, 7, 3],
                [9, 2, 1],
                [9, 3, 2],
                [9, 4, 3],
                [9, 5, 4],
                [9, 7, 6],
            ],
            "status": "unsolved",
            "moves": [
                {
                    "index": 1,
                    "kind": "write_mark",
                    "target": [1, 2],
                    "digit": 3,
                    "digit_before": None,
                    "struck_from": [],
                    "is_undone": False,
                },
                {
                    "index": 2,
                    "kind": "write_mark",
                    "target": [1, 1],
                    "digit": 3,
                    "digit_before": None,
                    "struck_from": [],
                    "is_undone": False,
                },
                {
                    "index": 3,
                    "kind": "place",
                    "target": [1, 1],
                    "digit": 3,
                    "digit_before": None,
                    "struck_from": [[1, 2]],
                    "is_undone": False,
                },
                {
                    "index": 4,
                    "kind": "place",
                    "target": [2, 1],
                    "digit": 5,
                    "digit_before": None,
                    "struck_from": [],
                    "is_undone": False,
                },
                {
                    "index": 5,
                    "kind": "erase",
                    "target": [2, 1],
                    "digit": None,
                    "digit_before": 5,
                    "struck_from": [],
                    "is_undone": False,
                },
                {
                    "index": 6,
                    "kind": "place",
                    "target": [2, 1],
                    "digit": 4,
                    "digit_before": None,
                    "struck_from": [],
                    "is_undone": True,
                },
            ],
            "checks": [
                {"index": 1, "after_move": 4, "target": [2, 1], "digit": 5, "is_right": False}
            ],
        }
    )


def test_a_solved_board_is_written_and_reopened_solved() -> None:
    board = Board.open(givens())
    board.write_mark(board.entry(1, 1), 1)
    for cell in board.marked:
        board.place(board.entry_at(cell.position), solution_at(cell.position))
    again = Board.reopen(board.write())
    hold_invariants(board, again)
    assert again.render() == board.render()
    assert again.render().splitlines()[0] == snapshot(
        "status: solved  full: yes  consistent: yes  undo: no  redo: no"
    )
    assert not again.can_undo


def test_writing_changes_nothing() -> None:
    board = played()
    before = board.render()
    board.write()
    assert board.render() == before


def test_reopening_is_exact() -> None:
    board = played()
    again = Board.reopen(board.write())
    hold_invariants(board, again)
    assert again.render() == board.render()
    assert again.write() == board.write()
    assert [m.target for m in again.moves] == [m.target for m in board.moves]
    assert [m.struck_from for m in again.moves] == [m.struck_from for m in board.moves]
    assert [c.target for c in again.checks] == [c.target for c in board.checks]
    for act in ("undo", "redo", "redo"):
        getattr(board, act)()
        getattr(again, act)()
        assert again.render() == board.render()
    assert again.render() == snapshot("""\
status: unsolved  full: no  consistent: yes  undo: yes  redo: no
r1   3   .   .  |  .   .   .  |  .   .   .
r2   4   .   .  |  .   .   .  | [1] [2] [3]
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
- r1c1: 3 (beneath a digit)
moves:
- 1 write_mark r1c2+3
- 2 write_mark r1c1+3
- 3 place r1c1=3 (was -) struck r1c2
- 4 place r2c1=5 (was -)
- 5 erase r2c1 (was 5)
- 6 place r2c1=4 (was -)
checks:
- 1 after move 4: r2c1=5 wrong
""")

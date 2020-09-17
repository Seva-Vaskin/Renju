import unittest
from renju.constants import *
from renju.board import Board
from renju import engine
import copy


class TestBoard(unittest.TestCase):
    def test_get_set_state(self):
        board = Board()
        board.set_state((0, 0), CellState.WHITE)
        self.assertEqual(board.get_cell_state((0, 0)), CellState.WHITE)
        board.set_state((6, 9), CellState.BLACK)
        self.assertEqual(board.get_cell_state((6, 9)), CellState.BLACK)
        board.set_state((6, 9), CellState.WHITE)
        self.assertEqual(board.get_cell_state((6, 9)), CellState.WHITE)
        with self.assertRaises(IndexError):
            board.get_cell_state((20, 20))
        with self.assertRaises(IndexError):
            board.get_cell_state((CELLS_IN_COLUMN, 3))
        with self.assertRaises(IndexError):
            board.set_state((CELLS_IN_COLUMN, CELLS_IN_ROW), CellState.WHITE)
        with self.assertRaises(IndexError):
            board.set_state((21, 65), CellState.EMPTY)

    def test_is_empty(self):
        board = Board()
        board.set_state((1, 4), CellState.WHITE)
        self.assertFalse(board.is_empty((1, 4)))
        board.set_state((1, 4), CellState.EMPTY)
        self.assertTrue(board.is_empty((1, 4)))
        self.assertTrue(board.is_empty((13, 2)))
        with self.assertRaises(IndexError):
            board.is_empty((CELLS_IN_COLUMN, 2))
        with self.assertRaises(IndexError):
            board.is_empty((58, 895))

    def test_do_move(self):
        board = Board()
        board.set_state((1, 2), CellState.WHITE)
        board.set_state((3, 4), CellState.BLACK)
        last_empty_cells = board.empty_cells
        last_who_moves = board.whose_move
        board.do_move((5, 7))
        self.assertEqual(last_empty_cells, board.empty_cells + 1)
        self.assertEqual(board.last_move_cell, (5, 7))
        self.assertNotEqual(board.whose_move, last_who_moves)
        with self.assertRaises(AssertionError):
            board.do_move((5, 7))
        with self.assertRaises(AssertionError):
            board.do_move((1, 2))

    def test_update_state(self):
        board = Board()
        self.assertEqual(board.state, BoardState.GAMING)
        board.update_state()
        # Тест ситуации, когда выигрвают чёрные
        self.assertEqual(board.state, BoardState.GAMING)
        for i in range(WIN_ROW_LENGTH):
            board.do_move((i, 0))
            if i + 1 != WIN_ROW_LENGTH:
                board.do_move((i * 2, 3))
        self.assertEqual(board.state, BoardState.BLACK_WINS)
        # Тест ситуации, когда выигрвают белые
        board.clear()
        for i in range(WIN_ROW_LENGTH):
            board.do_move((4, i * 2))
            board.do_move((10, i + 5))
        self.assertEqual(board.state, BoardState.WHITE_WINS)

    def test_try_do_move(self):
        board = Board()
        self.assertEqual(board.try_do_move((1, 2)), True)
        self.assertEqual(board.try_do_move((1, 2)), False)

    def test_find_wins_line(self):
        board = Board()
        self.assertEqual(board.find_wins_line(), None)
        for i in range(WIN_ROW_LENGTH):
            board.do_move((i, i))
            if i + 1 < WIN_ROW_LENGTH:
                self.assertEqual(board.find_wins_line(), None)
                board.do_move((CELLS_IN_COLUMN - 1 - i, CELLS_IN_ROW - 1 - i))
                self.assertEqual(board.find_wins_line(), None)
            else:
                ans1 = board.find_wins_line()
                ans2 = ((0, 0), (WIN_ROW_LENGTH - 1, WIN_ROW_LENGTH - 1))
                self.assertEqual(ans1, ans2)


class TestEngine(unittest.TestCase):
    def test_undo_move(self):
        b1 = Board()
        b2 = copy.deepcopy(b1)
        last_move_cell = b2.last_move_cell
        last_state = b2.state
        b2.do_move((10, 12))
        engine.undo_move(b2, last_move_cell, last_state)
        self.assertEqual(b1.last_move_cell, b2.last_move_cell)
        self.assertEqual(b1.state, b2.state)
        self.assertEqual(b1.whose_move, b2.whose_move)
        for row in range(CELLS_IN_COLUMN):
            for column in range(CELLS_IN_ROW):
                self.assertEqual(b1.cells[row][column], b2.cells[row][column])

    def test_do_computers_move(self):
        board = Board()
        try:
            for i in range(5):
                engine.do_computers_move(board)
                if board.state != BoardState.GAMING:
                    board.clear()
        except BaseException:
            self.fail("Engine делает некорректные ходы")


if __name__ == "__main__":
    unittest.main()

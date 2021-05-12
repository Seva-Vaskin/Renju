import unittest
from renju import const
from renju.board import Board, CellState, BoardState, Player
from renju.game import Game
from renju import engine
import copy


class TestBoard(unittest.TestCase):
    def test_get_set_state(self):
        board = Board()
        board[0, 0] = CellState.WHITE
        self.assertEqual(board[0, 0], CellState.WHITE)
        board[6, 9] = CellState.BLACK
        self.assertEqual(board[6, 9], CellState.BLACK)
        board[6, 9] = CellState.WHITE
        self.assertEqual(board[6, 9], CellState.WHITE)
        with self.assertRaises(IndexError):
            board[20, 20]
        with self.assertRaises(IndexError):
            board[const.BOARD_SIZE[0], 3]
        with self.assertRaises(IndexError):
            board[const.BOARD_SIZE] = CellState.WHITE
        with self.assertRaises(IndexError):
            board[21, 65] = CellState.EMPTY

    def test_is_empty(self):
        board = Board()
        board[1, 4] = CellState.WHITE
        self.assertTrue(board[1, 4])
        board[1, 4] = CellState.EMPTY
        self.assertFalse(board[1, 4])
        self.assertFalse(board[13, 2])

    def test_do_move(self):
        board = Board()
        board.do_move((1, 2))
        board.do_move((3, 4))
        board_copy = copy.deepcopy(board)
        pos = (5, 7)
        board.do_move(pos)
        for row in range(const.BOARD_SIZE[0]):
            for column in range(const.BOARD_SIZE[1]):
                if (row, column) == pos:
                    self.assertNotEqual(board[row, column],
                                        board_copy[row, column])
                else:
                    self.assertEqual(board[row, column],
                                     board_copy[row, column])
        self.assertNotEqual(board.whose_move, board_copy.whose_move)
        self.assertEqual(board.state, board_copy.state)
        self.assertEqual(len(board.moves), len(board_copy.moves) + 1)
        for i in range(len(board_copy.moves)):
            self.assertEqual(board.moves[i], board_copy.moves[i])
        self.assertEqual(board.moves[-1], pos)
        with self.assertRaises(AssertionError):
            board.do_move(pos)
        with self.assertRaises(AssertionError):
            board.do_move((1, 2))

    def test_undo_move(self):
        board = Board()
        with self.assertRaises(BaseException):
            board.undo_move()
        board.do_move((0, 0))
        board.undo_move()
        for row in range(const.BOARD_SIZE[0]):
            for column in range(const.BOARD_SIZE[1]):
                self.assertEqual(board[row, column], CellState.EMPTY)
        self.assertEqual(board.whose_move, Player.BLACK)
        self.assertEqual(board.state, BoardState.GAMING)
        self.assertFalse(board.moves)

    def test_update_state(self):
        board = Board()
        self.assertEqual(board.state, BoardState.GAMING)
        board.update_state()
        # Тест ситуации, когда выигрвают чёрные
        self.assertEqual(board.state, BoardState.GAMING)
        for i in range(const.WIN_ROW_LENGTH):
            board.do_move((i, 0))
            if i + 1 != const.WIN_ROW_LENGTH:
                board.do_move((i * 2, 3))
        self.assertEqual(board.state, BoardState.BLACK_WINS)
        # Тест ситуации, когда выигрвают белые
        board = Board()
        for i in range(const.WIN_ROW_LENGTH):
            board.do_move((4, i * 2))
            board.do_move((10, i + 5))
        self.assertEqual(board.state, BoardState.WHITE_WINS)
        # Тест ситуации, когда ничья
        memorized_board_size = const.BOARD_SIZE
        const.BOARD_SIZE = (3, 3)
        board = Board()
        for row in range(const.BOARD_SIZE[0]):
            for column in range(const.BOARD_SIZE[1]):
                board.do_move((row, column))
        self.assertEqual(board.state, BoardState.DRAW)
        const.BOARD_SIZE = memorized_board_size

    def test_find_wins_line(self):
        board = Board()
        for i in range(const.WIN_ROW_LENGTH):
            board.do_move((i, i))
            if i + 1 < const.WIN_ROW_LENGTH:
                board.do_move((const.BOARD_SIZE[0] - 1 - i,
                               const.BOARD_SIZE[1] - 1 - i))
            else:
                ans_1 = board.find_wins_line()
                ans_2 = ((0, 0),
                         (const.WIN_ROW_LENGTH - 1, const.WIN_ROW_LENGTH - 1))
                ans_3 = (ans_2[1], ans_2[0])
                self.assertTrue(ans_1 == ans_2 or ans_1 == ans_3)


class TestEngine(unittest.TestCase):
    def test_rate_function(self):
        board = Board()
        for i in range(const.WIN_ROW_LENGTH):
            board.do_move((i, 0))
            board.do_move((i, 1))
        self.assertEqual(engine.rate_function(board), const.MINIMAX_INF)
        board = Board()
        board[1, 2] = CellState.BLACK
        board[2, 3] = CellState.BLACK
        self.assertGreater(engine.rate_function(board), 0)

    def test_minimax(self):
        board = Board()
        self.assertEqual(engine.minimax(board, const.MAX_MINIMAX_DEPTH)[0],
                         engine.rate_function(board))
        for i in range(const.WIN_ROW_LENGTH - 1):
            board[i, 0] = CellState.BLACK
        ans_1 = engine.minimax(board)
        ans_2 = (const.MINIMAX_INF, (const.WIN_ROW_LENGTH - 1, 0))
        self.assertEqual(ans_1, ans_2)
        board = Board()
        memorized_board_size = const.BOARD_SIZE
        const.BOARD_SIZE = (3, 3)
        for row in range(const.BOARD_SIZE[0]):
            for column in range(const.BOARD_SIZE[1]):
                board.do_move((row, column))
        board.undo_move()
        ans_1 = engine.minimax(board)
        ans_2 = (0, (const.BOARD_SIZE[0] - 1, const.BOARD_SIZE[1] - 1))
        self.assertEqual(ans_1, ans_2)
        const.BOARD_SIZE = memorized_board_size

    def test_do_computers_move(self):
        game = Game()
        try:
            for i in range(5):
                engine.do_computers_move(game)
        except BaseException:
            self.fail("Engine делает некорректные ходы")


if __name__ == "__main__":
    unittest.main()

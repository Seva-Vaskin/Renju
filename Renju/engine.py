"""Модуль, реализующий действия компьютера."""

from .board import Board
from .constants import *


def minimax(board, depth=0, alpha=MINIMAX_INF + 1):
    """Возвращает оценку ситуации на доске и клетку,
    в которую нужно сделать ход.
    """
    if depth == MAX_MINIMAX_DEPTH:
        return rate_function(board), (-1, -1)
    rate = -MINIMAX_INF - 1
    move = (-1, -1)
    for row in range(CELLS_IN_COLUMN):
        for column in range(CELLS_IN_ROW):
            if not board.is_empty((row, column)):
                continue
            memorized_last_move = board.last_move_cell
            memorized_board_state = board.state
            board.do_move((row, column))
            if board.state in (BoardState.WHITE_WINS, BoardState.BLACK_WINS):
                undo_move(board, memorized_last_move, memorized_board_state)
                return MINIMAX_INF, (row, column)
            elif board.state == BoardState.DRAW:
                cur_rate = 0
            else:
                cur_rate = -minimax(board, depth + 1, -rate)[0]
            undo_move(board, memorized_last_move, memorized_board_state)
            if cur_rate >= alpha:
                return cur_rate, (-1, -1)
            if rate < cur_rate or move == (-1, -1):
                rate = cur_rate
                move = (row, column)
    return rate, move


def rate_function(board):
    """Возвращает число - оценку ситуации на доске для того,
    кто сейчас будет ходить.
    """
    if board.state in (BoardState.WHITE_WINS, BoardState.BLACK_WINS):
        return MINIMAX_INF
    counter = [0] * WIN_ROW_LENGTH
    k = [0, 0, 100, 200, 4000000]
    vectors = [(1, -1), (1, 0), (1, 1), (0, 1)]
    for row in range(CELLS_IN_COLUMN):
        for column in range(CELLS_IN_ROW):
            for vector in vectors:
                if not Board.in_field((row + vector[0] * (WIN_ROW_LENGTH - 1),
                                       column + vector[1] * (
                                               WIN_ROW_LENGTH - 1))):
                    continue
                r = row
                c = column
                count_black = 0
                count_white = 0
                for i in range(WIN_ROW_LENGTH):
                    if board.get_cell_state((r, c)) == CellState.BLACK:
                        count_black += 1
                    elif board.get_cell_state((r, c)) == CellState.WHITE:
                        count_white += 1
                    r += vector[0]
                    c += vector[1]
                if count_black != 0 and count_white != 0:
                    continue
                if board.whose_move == Player.BLACK:
                    if count_black != 0:
                        counter[count_black] += 1
                    elif count_white != 0:
                        counter[count_white] -= 1
                else:
                    if count_white != 0:
                        counter[count_white] += 1
                    elif count_black != 0:
                        counter[count_black] -= 1

    f = 0
    for i in range(WIN_ROW_LENGTH):
        f += k[i] * counter[i]
    return f


def do_computers_move(board):
    """Делает ход компьютера."""
    pos = minimax(board)[1]
    board.do_move(pos)


def undo_move(board, last_move_cell, last_board_state):
    """Отменяет ход."""
    board.set_state(board.last_move_cell, CellState.EMPTY)
    board.empty_cells += 1
    if board.whose_move == Player.BLACK:
        board.whose_move = Player.WHITE
    else:
        board.whose_move = Player.BLACK
    board.last_move_cell = last_move_cell
    board.state = last_board_state

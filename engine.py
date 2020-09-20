"""Модуль, реализующий действия компьютера."""

from .board import Board, BoardState, CellState, Player
from . import const
from typing import Tuple


def minimax(board: Board,
            depth: int = 0) -> Tuple[int, Tuple[int, int]]:
    """Возвращает оценку ситуации на доске и клетку,
    в которую нужно сделать ход.
    """
    if depth == const.MAX_MINIMAX_DEPTH:
        return rate_function(board), (-1, -1)
    rate = -const.MINIMAX_INF - 1
    move = (-1, -1)
    for row in range(const.BOARD_SIZE[0]):
        for column in range(const.BOARD_SIZE[1]):
            if board[row, column]:
                continue
            board.do_move((row, column))
            if board.state in (BoardState.WHITE_WINS, BoardState.BLACK_WINS):
                board.undo_move()
                return const.MINIMAX_INF, (row, column)
            elif board.state == BoardState.DRAW:
                cur_rate = 0
            else:
                cur_rate = -minimax(board, depth + 1)[0]
            board.undo_move()
            if rate < cur_rate or move == (-1, -1):
                rate = cur_rate
                move = (row, column)
    return rate, move


def rate_function(board: Board) -> int:
    """Возвращает число - оценку ситуации на доске для того,
    кто сейчас будет ходить.
    """
    if board.state in (BoardState.WHITE_WINS, BoardState.BLACK_WINS):
        return const.MINIMAX_INF
    score = 0
    k = [0, 0, 100, 200, 4000000]
    vectors = [(1, -1), (1, 0), (1, 1), (0, 1)]
    for row in range(const.BOARD_SIZE[0]):
        for column in range(const.BOARD_SIZE[1]):
            for vector in vectors:
                if not Board.in_field(
                        (row + vector[0] * (const.WIN_ROW_LENGTH - 1),
                         column + vector[1] * (const.WIN_ROW_LENGTH - 1))):
                    continue
                r = row
                c = column
                count_black = 0
                count_white = 0
                for i in range(const.WIN_ROW_LENGTH):
                    if board[r, c] == CellState.BLACK:
                        count_black += 1
                    elif board[r, c] == CellState.WHITE:
                        count_white += 1
                    r += vector[0]
                    c += vector[1]
                if count_black != 0 and count_white != 0:
                    continue
                if board.whose_move == Player.BLACK:
                    if count_black != 0:
                        score += k[count_black]
                    elif count_white != 0:
                        score -= k[count_white]
                else:
                    if count_white != 0:
                        score += k[count_white]
                    elif count_black != 0:
                        score -= k[count_black]
    return score


def do_computers_move(board: Board) -> None:
    """Делает ход компьютера."""
    pos = minimax(board)[1]
    board.do_move(pos)


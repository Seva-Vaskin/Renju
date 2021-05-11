"""Модуль, отвечающий за игровое поле."""

from . import const
from typing import Tuple
import enum


class CellState(enum.IntEnum):
    """Описывает состояние клетки:
    EMPTY - клетка пустая,
    BLACK - клетка занята чёрной фишкой,
    WHITE - клетка занята белой фишкой.
    """
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class BoardState(enum.IntEnum):
    """Описывает игровую партию:
    GAMING - игра продолжается,
    BLACK_WINS - игра завершена, чёрные выиграли,
    WHITE_WINS - игра завершена, белые выиграли,
    DRAW - игра завершена, объявлена ничья.
    """
    GAMING = 0
    BLACK_WINS = 1
    WHITE_WINS = 2
    DRAW = 3


class Player(enum.IntEnum):
    """Описывает соперников:
    BLACK - чёрный игрок,
    WHITE - белый игрок.
    """
    BLACK = 0
    WHITE = 1


class Board:
    """Описывает игровое поле."""

    def __init__(self) -> None:
        self.cells = [[CellState.EMPTY] * const.BOARD_SIZE[1] for i in
                      range(const.BOARD_SIZE[0])]
        self.whose_move = Player.BLACK
        self.state = BoardState.GAMING
        self.moves = list()

    def __getitem__(self, pos: Tuple[int, int]) -> CellState:
        """Возвращает состояние клетки."""
        return self.cells[pos[0]][pos[1]]

    def __setitem__(self, pos: Tuple[int, int], state: CellState) -> None:
        """Устанавливает в клетку необходимое состояние."""
        self.cells[pos[0]][pos[1]] = state

    def do_move(self, pos: Tuple[int, int]) -> None:
        """Делает ход. Пересчитывает все атрибуты класса."""
        assert not self[pos], "Ходить можно только в пусую клетку."
        self.moves.append(pos)
        if self.whose_move == Player.BLACK:
            self[pos] = CellState.BLACK
            self.whose_move = Player.WHITE
        else:
            self[pos] = CellState.WHITE
            self.whose_move = Player.BLACK
        self.update_state()

    def undo_move(self) -> None:
        """Отменяет ход. Пересчитывает все атрибуты класса."""
        self[self.moves[-1]] = CellState.EMPTY
        if self.whose_move == Player.BLACK:
            self.whose_move = Player.WHITE
        else:
            self.whose_move = Player.BLACK
        self.state = BoardState.GAMING
        self.moves.pop()

    @staticmethod
    def in_field(pos: Tuple[int, int]) -> bool:
        """Проверяет, что клетка находится в пределах игрового поля."""
        return 0 <= pos[0] < const.BOARD_SIZE[0] and \
            0 <= pos[1] < const.BOARD_SIZE[1]

    def find_max_line(self, start: Tuple[int, int]) \
            -> Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Возвращает длину, а также координаты начала и конца самой длинной
        линии, состоящей из фишек одного цвета, проходящей через клетку start.
        """
        max_length = 1
        line = (start, start)
        vectors = [(1, -1), (1, 0), (1, 1), (0, 1)]
        for vector in vectors:
            length = 1
            pos_1 = (start[0] + vector[0], start[1] + vector[1])
            # Двигаем pos_1, пока в pos_1 стоит фишка того же цвета,
            # что и фишка в start.
            while Board.in_field(pos_1) and self[pos_1] == self[start]:
                length += 1
                pos_1 = (pos_1[0] + vector[0], pos_1[1] + vector[1])
            # Сдвигаем pos_1 обратно, чтобы pos_1 указывал на фишку одного
            # цвета, что и start.
            pos_1 = (pos_1[0] - vector[0], pos_1[1] - vector[1])
            # Двигаем pos_2 аналогично движению pos_1, но в противоположную
            # сторону от start.
            pos_2 = (start[0] - vector[0], start[1] - vector[1])
            while Board.in_field(pos_2) and self[pos_2] == self[start]:
                length += 1
                pos_2 = (pos_2[0] - vector[0], pos_2[1] - vector[1])
            pos_2 = (pos_2[0] + vector[0], pos_2[1] + vector[1])
            if max_length < length:
                max_length = length
                line = (pos_1, pos_2)
        return max_length, line

    def update_state(self) -> None:
        """Обновляет состояние доски."""
        if not self.moves:
            self.state = BoardState.GAMING
            return
        max_length = self.find_max_line(self.moves[-1])[0]
        if max_length >= const.WIN_ROW_LENGTH:
            if self[self.moves[-1]] == CellState.BLACK:
                self.state = BoardState.BLACK_WINS
            else:
                self.state = BoardState.WHITE_WINS
        elif len(self.moves) == const.BOARD_SIZE[0] * const.BOARD_SIZE[1]:
            self.state = BoardState.DRAW
        else:
            self.state = BoardState.GAMING

    def find_wins_line(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Возвращает координаты начала и конца выигрышной линии."""
        return self.find_max_line(self.moves[-1])[1]

"""Модуль, отвечающий за игровое поле."""

from .constants import *


class Board:
    """Описывает игровое поле."""

    def __init__(self):
        self.cells = [[CellState.EMPTY] * CELLS_IN_ROW for i in
                      range(CELLS_IN_COLUMN)]
        self.whose_move = Player.BLACK
        self.empty_cells = CELLS_IN_ROW * CELLS_IN_COLUMN
        self.last_move_cell = (-1, -1)
        self.state = BoardState.GAMING

    def set_state(self, pos, state):
        """Устанавливает в клетку необходимое состояние."""
        self.cells[pos[0]][pos[1]] = state

    def get_cell_state(self, pos):
        """Возвращает состояние клетки."""
        return self.cells[pos[0]][pos[1]]

    def is_empty(self, pos):
        """Возвращает True, если клетка пустая, False, если клетка занята."""
        return self.get_cell_state(pos) == CellState.EMPTY

    def do_move(self, pos):
        """Делает ход. Пересчитывает все атрибуты класса."""
        assert self.is_empty(pos), "Ходить можно только в пусую клетку"
        self.empty_cells -= 1
        self.last_move_cell = pos
        if self.whose_move == Player.BLACK:
            self.set_state(pos, CellState.BLACK)
            self.whose_move = Player.WHITE
        else:
            self.set_state(pos, CellState.WHITE)
            self.whose_move = Player.BLACK
        self.update_state()

    def try_do_move(self, pos):
        """Если клетка занята, возвращает False,
        иначе делает ход и возвращает True.
        """
        if not self.is_empty(pos):
            return False
        self.do_move(pos)
        return True

    @staticmethod
    def in_field(pos):
        """Проверяет, что клетка находится в пределах игрового поля."""
        return 0 <= pos[0] < CELLS_IN_ROW and 0 <= pos[1] < CELLS_IN_COLUMN

    def update_state(self):
        """Обновляет состояние доски."""
        if self.last_move_cell == (-1, -1):
            self.state = BoardState.GAMING
            return

        delta = [(1, -1), (1, 0), (1, 1), (0, 1)]
        for d in delta:
            stones_count_in_row = 1
            # Идём по вектору d, считаем количество фишек
            # На второй итерации идём по -d
            for i in range(2):
                pos = (
                    self.last_move_cell[0] + d[0],
                    self.last_move_cell[1] + d[1])
                while Board.in_field(pos) and \
                        self.get_cell_state(pos) == self.get_cell_state(
                        self.last_move_cell):
                    stones_count_in_row += 1
                    pos = (pos[0] + d[0], pos[1] + d[1])
                d = (-d[0], -d[1])
            if stones_count_in_row >= WIN_ROW_LENGTH:
                if self.get_cell_state(self.last_move_cell) == CellState.BLACK:
                    self.state = BoardState.BLACK_WINS
                    return
                else:
                    self.state = BoardState.WHITE_WINS
                    return
        if self.empty_cells == 0:
            self.state = BoardState.DRAW
        else:
            self.state = BoardState.GAMING

    def find_wins_line(self):
        delta = [(1, -1), (1, 0), (1, 1), (0, 1)]
        for row in range(CELLS_IN_COLUMN):
            for column in range(CELLS_IN_ROW):
                if self.is_empty((row, column)):
                    continue
                for d in delta:
                    r = row + d[0]
                    c = column + d[1]
                    count = 1
                    while self.in_field((r, c)) and \
                            self.get_cell_state((row, column)) == \
                            self.get_cell_state((r, c)) and count < 5:
                        count += 1
                        r += d[0]
                        c += d[1]
                    if count == WIN_ROW_LENGTH:
                        return (row, column), (r - d[0], c - d[1])

    def clear(self):
        """Очищает игровое поле."""
        self.__init__()

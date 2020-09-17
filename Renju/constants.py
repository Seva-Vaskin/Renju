"""Модуль, описывающий константы, используемые в проекте."""

import enum


class CellState(enum.Enum):
    """Описывает состояние клетки:
    EMPTY - клетка пустая,
    BLACK - клетка занята чёрной фишкой,
    WHITE - клетка занята белой фишкой.
    """
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class BoardState(enum.Enum):
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


class Color:
    """Коды RGB для цветов, необходимых для реализации игры."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


class Player(enum.Enum):
    """Описывает соперников:
    BLACK - чёрный игрок,
    WHITE - белый игрок.
    """
    BLACK = 0
    WHITE = 1


# Размеры поля в клетках
CELLS_IN_COLUMN = 15
CELLS_IN_ROW = 15

# Размер клетки в пикселях
CELL_SIZE = 30
# Толщина линий разметки на экране
LINE_WIDTH = 1
# Длина выигрышного ряда
WIN_ROW_LENGTH = 5
# Размеры игрового окна
WINDOW_HEIGHT = CELLS_IN_COLUMN * CELL_SIZE
WINDOW_WIDTH = CELLS_IN_ROW * CELL_SIZE
# Максимальная глубина рекурсии в алгоритме минимакс
MAX_MINIMAX_DEPTH = 1
# Условная бесконечность в алгоритме минимакс
MINIMAX_INF = 10 ** 10

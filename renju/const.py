"""Модуль, описывающий константы, используемые в проекте."""

from pathlib import Path


class Color:
    """Коды RGB для цветов, необходимых для реализации игры."""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)


# Размеры поля в клетках (высота, ширина)
BOARD_SIZE = (16, 16)

# Размер клетки в пикселях
CELL_SIZE = 30
# Толщина линий разметки на экране
LINE_WIDTH = 1
# Высота нижнего меню в пикселях
MENU_HEIGHT = 40
# Размеры игрового окна в пикселях
WINDOW_HEIGHT = CELL_SIZE * BOARD_SIZE[0] + MENU_HEIGHT
WINDOW_WEIGHT = CELL_SIZE * BOARD_SIZE[1]
# Координаты центра меню
MENU_CENTER = (WINDOW_WEIGHT // 2, WINDOW_HEIGHT - MENU_HEIGHT // 2)
# Время отведённое на игру в секундах
GAME_TIME_LIMIT = 60
# Длина выигрышного ряда
WIN_ROW_LENGTH = 5
# Максимальная глубина рекурсии в алгоритме минимакс
MAX_MINIMAX_DEPTH = 1
# Условная бесконечность в алгоритме минимакс
MINIMAX_INF = 10 ** 10
# Путь до файла сохранения игры
SAVE_PATH = Path("./save.txt")

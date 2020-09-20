"""Модуль, отвечающий за игровое окно."""

import pygame
from . import const
from . import engine
from .board import Board, BoardState, CellState, Player
from typing import Tuple

screen: type(pygame.display)


def init() -> None:
    """Инициализирует pygame. Создаёт игровое окно."""
    pygame.init()
    global screen
    height = const.BOARD_SIZE[0] * const.CELL_SIZE
    weight = const.BOARD_SIZE[1] * const.CELL_SIZE
    screen = pygame.display.set_mode((height, weight))
    pygame.display.set_caption('Рендзю')
    draw_background()
    update()


def close() -> None:
    """Прекращает работу pygame. Закрывает игровое окно."""
    pygame.display.quit()
    pygame.quit()


def draw_background() -> None:
    """Рисует разметку игрового поля."""
    screen.fill(const.Color.WHITE)
    for i in range(const.BOARD_SIZE[0]):
        pos1 = get_cell_center((i, 0))
        pos2 = get_cell_center((i, const.BOARD_SIZE[1] - 1))
        pygame.draw.line(screen, const.Color.BLACK, pos1, pos2,
                         const.LINE_WIDTH)
    for i in range(const.BOARD_SIZE[1]):
        pos1 = get_cell_center((0, i))
        pos2 = get_cell_center((const.BOARD_SIZE[0] - 1, i))
        pygame.draw.line(screen, const.Color.BLACK, pos1, pos2,
                         const.LINE_WIDTH)


def draw_board(board: Board) -> None:
    """Рисует фишки нужного цвета."""
    for row in range(const.BOARD_SIZE[0]):
        for column in range(const.BOARD_SIZE[1]):
            pos = get_cell_center((row, column))
            radius = const.CELL_SIZE // 2
            if board.cells[row][column] == CellState.BLACK:
                pygame.draw.circle(screen, const.Color.BLACK, pos, radius)
            elif board.cells[row][column] == CellState.WHITE:
                pygame.draw.circle(screen, const.Color.WHITE, pos, radius)
                pygame.draw.circle(screen, const.Color.BLACK, pos, radius, 1)
    if board.state in (BoardState.WHITE_WINS, BoardState.BLACK_WINS):
        pos1, pos2 = board.find_wins_line()
        pos1 = get_cell_center(pos1)
        pos2 = get_cell_center(pos2)
        pygame.draw.line(screen, const.Color.RED, pos1, pos2,
                         2 * const.LINE_WIDTH)
    update()


def get_cell_center(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Возвращает координаты центра клетки на экране."""
    return pos[1] * const.CELL_SIZE + const.CELL_SIZE // 2, \
           pos[0] * const.CELL_SIZE + const.CELL_SIZE // 2


def mouse_pos_to_cell(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Вычисляет позицию мышки на игровом поле."""
    x_mouse, y_mouse = pos
    row = y_mouse // const.CELL_SIZE
    column = x_mouse // const.CELL_SIZE
    return row, column


def update() -> None:
    """Обновляет игровое поле."""
    pygame.display.update()


def events_processing(board: Board) -> bool:
    """Реакция на действия пользователя.
    Возвращает True, если игра продолжается, иначе False.
    """
    pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                if board.state != BoardState.GAMING:
                    board.clear()
                    draw_background()
                    update()
                    continue
                mouse_pos = pygame.mouse.get_pos()
                pos = mouse_pos_to_cell(mouse_pos)
                if not board.try_do_move(pos):
                    continue
                draw_board(board)
                if board.state == BoardState.GAMING:
                    engine.do_computers_move(board)
                    draw_board(board)
            elif event.button == 3:  # ПКМ
                board.undo_move()
                if board.whose_move != Player.BLACK:
                    board.undo_move()
                draw_background()
                draw_board(board)

    return True

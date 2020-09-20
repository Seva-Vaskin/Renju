"""Модуль, отвечающий за игровое окно."""

import pygame
from renju.constants import *
from renju import engine

screen: type(pygame.display)


def init():
    """Инициализирует pygame. Создаёт игровое окно."""
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    pygame.display.set_caption('Рендзю')
    draw_background()
    update()


def close():
    """Прекращает работу pygame. Закрывает игровое окно."""
    pygame.display.quit()
    pygame.quit()


def draw_background():
    """Рисует разметку игрового поля."""
    screen.fill(Color.WHITE)
    for i in range(CELLS_IN_COLUMN):
        pos1 = get_cell_center((i, 0))
        pos2 = get_cell_center((i, CELLS_IN_ROW - 1))
        pygame.draw.line(screen, Color.BLACK, pos1, pos2, LINE_WIDTH)
    for i in range(CELLS_IN_ROW):
        pos1 = get_cell_center((0, i))
        pos2 = get_cell_center((CELLS_IN_COLUMN - 1, i))
        pygame.draw.line(screen, Color.BLACK, pos1, pos2, LINE_WIDTH)


def draw_board(board):
    """Рисует фишки нужного цвета."""
    for row in range(CELLS_IN_COLUMN):
        for column in range(CELLS_IN_ROW):
            pos = get_cell_center((row, column))
            radius = CELL_SIZE // 2
            if board.cells[row][column] == CellState.BLACK:
                pygame.draw.circle(screen, Color.BLACK, pos, radius)
            elif board.cells[row][column] == CellState.WHITE:
                pygame.draw.circle(screen, Color.WHITE, pos, radius)
                pygame.draw.circle(screen, Color.BLACK, pos, radius, 1)
    if board.state in (BoardState.WHITE_WINS, BoardState.BLACK_WINS):
        pos1, pos2 = board.find_wins_line()
        pos1 = get_cell_center(pos1)
        pos2 = get_cell_center(pos2)
        pygame.draw.line(screen, Color.RED, pos1, pos2, 2 * LINE_WIDTH)
    update()


def get_cell_center(pos):
    """Возвращает координаты центра клетки на экране."""
    return pos[1] * CELL_SIZE + CELL_SIZE // 2, \
           pos[0] * CELL_SIZE + CELL_SIZE // 2


def mouse_pos_to_cell(pos):
    """Вычисляет позицию мышки на игровом поле."""
    x_mouse, y_mouse = pos
    row = y_mouse // CELL_SIZE
    column = x_mouse // CELL_SIZE
    return row, column


def update():
    """Обновляет игровое поле."""
    pygame.display.update()


def events_processing(board):
    """Реакция на действия пользователя.
    Возвращает True, если игра продолжается, иначе False.
    """
    pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
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

    return True

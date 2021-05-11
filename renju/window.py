"""Модуль, отвечающий за игровое окно."""

import pygame
from . import const, engine
from .board import BoardState, CellState, Player
from .game import Game
from .saver import Saver
from typing import Tuple
import time

screen: type(pygame.display)


def init() -> None:
    """Инициализирует pygame. Создаёт игровое окно."""
    pygame.init()
    global screen
    screen = pygame.display.set_mode(
        (const.WINDOW_WEIGHT, const.WINDOW_HEIGHT))
    pygame.display.set_caption('Рендзю')
    draw_background()
    update()


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
    update()


def draw_board(game: Game) -> None:
    """Рисует фишки нужного цвета."""
    board = game.board
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


def draw_text_in_menu(text: str) -> None:
    """Рисует заданный текст в меню."""
    menu_font = pygame.font.Font(pygame.font.get_default_font(),
                                 const.MENU_HEIGHT)
    rendered_text = menu_font.render(text, True, const.Color.BLACK)
    text_rect = rendered_text.get_rect()
    text_rect.center = const.MENU_CENTER
    screen.blit(rendered_text, text_rect)
    update()


def draw_time(game: Game) -> None:
    """Рисует время игроков до конца партии."""
    times = tuple(int(i) for i in game.get_times())
    text = "%02d:%02d / %02d:%02d" % (times[0] // 60, times[0] % 60,
                                      times[1] // 60, times[1] % 60)
    draw_text_in_menu(text)


def draw_game_result(game: Game) -> None:
    """Рисует результат игры."""
    game_state = game.board.state
    assert game_state != BoardState.GAMING
    if game_state == BoardState.BLACK_WINS:
        text = "Чёрные выиграли"
    elif game_state == BoardState.WHITE_WINS:
        text = "Белые выиграли"
    else:
        text = "Ничья"
    draw_text_in_menu(text)


def draw_menu(game: Game) -> None:
    """Рисует меню."""
    menu_rect = pygame.Rect(0, const.WINDOW_HEIGHT - const.MENU_HEIGHT,
                            const.WINDOW_WEIGHT, const.MENU_HEIGHT)
    pygame.draw.rect(screen, const.Color.WHITE, menu_rect)
    if game.board.state == BoardState.GAMING:
        draw_time(game)
    else:
        draw_game_result(game)


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


def try_draw_menu(game: Game) -> None:
    """Пытается нарисовать меню, но не чаще, чем раз в секунду."""
    if not hasattr(try_draw_menu, "last_time"):
        try_draw_menu.last_time = time.time()
        draw_time(game)
        return
    now_time = time.time()
    if now_time - try_draw_menu.last_time >= 1:
        try_draw_menu.last_time = now_time
        draw_menu(game)


def process_lmb_event(game: Game):
    """Обработка события нажатия ЛКМ."""
    board = game.board
    if board.state != BoardState.GAMING:
        game.restart()
        draw_background()
        draw_menu(game)
        return
    mouse_pos = pygame.mouse.get_pos()
    pos = mouse_pos_to_cell(mouse_pos)
    if not game.try_do_move(pos):
        return
    draw_board(game)
    if board.state == BoardState.GAMING:
        engine.do_computers_move(game)
        draw_board(game)


def process_rmb_event(game: Game):
    """Обработка события нажатия ПКМ."""
    game.undo_move()
    if game.board.whose_move != Player.BLACK:
        game.undo_move()
    draw_background()
    draw_board(game)
    draw_menu(game)


def process_quit_event(board: Game):
    """Прекращает работу pygame. Закрывает игровое окно."""
    pygame.display.quit()
    pygame.quit()
    Saver.save_game(board)


def process_events(game: Game) -> bool:
    """Реакция на действия пользователя.
    Возвращает True, если игра продолжается, иначе False.
    """
    pygame.time.Clock().tick(10)
    game.check_time()
    try_draw_menu(game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_quit_event(game)
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                process_lmb_event(game)
            elif event.button == 3:  # ПКМ
                process_rmb_event(game)
    return True

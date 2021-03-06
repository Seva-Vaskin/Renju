#!/usr/bin/env python3
import sys
import argparse

ERROR_PYTHON_VERSION = 1
ERROR_MODULES_MISSING = 2
ERROR_PYGAME_MISSING = 3
ERROR_PYGAME_VERSION = 4

if sys.version_info < (3, 6):
    print('Используйте python >= 3.6', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

try:
    from renju import game, window, loader
except Exception as e:
    print('Игровые модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

try:
    import pygame
except ImportError:
    print('Модуль pygame не найден', file=sys.stderr)
    sys.exit(ERROR_PYGAME_MISSING)

if pygame.vernum < (1, 9, 6):
    print('Используйте pygame >= 1.9.6', file=sys.stderr)
    sys.exit(ERROR_PYGAME_VERSION)


def parse_args() -> None:
    """Парсинг аргуметов запуска."""
    try:
        f = open('help.txt', encoding='utf-8')
        help_text = f.read()
        f.close()
    except FileNotFoundError:
        help_text = ''
    parser = argparse.ArgumentParser(
        description=help_text,
    )
    parser.parse_args()


if __name__ == '__main__':
    parse_args()
    window.init()
    try:
        field = loader.Loader.load_game()
    except BaseException:
        field = game.Game()
    window.draw_board(field)
    window.try_draw_menu(field)
    running = True
    while running:
        running = window.process_events(field)

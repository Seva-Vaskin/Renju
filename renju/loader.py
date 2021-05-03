from .game import Game
from . import const
import time


class Loader:
    """Отвечает за загрузку игры."""

    @staticmethod
    def load_game() -> Game:
        """Загружает игру."""
        game = Game()
        board = game.board
        with const.SAVE_PATH.open("r") as f:
            for line in f.readlines():
                x, y, duration = line.split()
                x = int(x)
                y = int(y)
                duration = float(duration)
                game.players_times[board.whose_move.value] -= duration
                game.moves_durations.append(duration)
                game.board.do_move((x, y))
        game.last_event_time = time.time()
        return game

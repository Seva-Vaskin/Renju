from .game import Game
from . import const


class Saver:
    """Отвечает за сохранение игры."""

    @staticmethod
    def save_game(game: Game) -> None:
        """Сохраняет игру."""
        with const.SAVE_PATH.open("w") as f:
            for i in range(len(game.board.moves)):
                move_pos = game.board.moves[i]
                move_duration = game.moves_durations[i]
                f.write("%d %d %.4f\n" % (move_pos[0], move_pos[1],
                                          move_duration))

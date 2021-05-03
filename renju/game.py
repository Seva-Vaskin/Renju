from .board import Board, Player, BoardState
from . import const
import time
from typing import Tuple


class Game:
    """Описывает игровой процесс."""

    def __init__(self):
        self.board = Board()
        self.moves_durations = list()
        self.players_times = [const.GAME_TIME_LIMIT for i in range(2)]
        self.last_event_time = time.time()

    def do_move(self, pos: Tuple[int, int]) -> None:
        """Делает ход. Пересчитывает все атрибуты класса."""
        cur_time = time.time()
        move_duration = cur_time - self.last_event_time
        self.last_event_time = cur_time
        self.moves_durations.append(move_duration)
        self.players_times[self.board.whose_move.value] -= move_duration
        self.board.do_move(pos)

    def try_do_move(self, pos: Tuple[int, int]) -> bool:
        """Если клетка занята, возвращает False,
        иначе делает ход и возвращает True.
        """
        if self.board[pos]:
            return False
        self.do_move(pos)
        return True

    def undo_move(self) -> None:
        """Отменяет ход. Пересчитывает все атрибуты класса."""
        if not self.board.moves:
            self.players_times = [const.GAME_TIME_LIMIT for i in range(2)]
            self.last_event_time = time.time()
            return
        self.board.undo_move()
        self.players_times[self.board.whose_move.value] \
            += self.moves_durations[-1]
        self.moves_durations.pop()
        self.last_event_time = time.time()

    def get_times(self) -> Tuple[float, float]:
        """Возвращает время игроков до конца партии."""
        t = [i for i in self.players_times]
        t[self.board.whose_move.value] -= time.time() - self.last_event_time
        return t[0], t[1]

    def check_time(self) -> None:
        """Проверяет, не вышло ли время у игроков."""
        cur_times = self.get_times()
        if cur_times[Player.BLACK.value] < 0:
            self.board.state = BoardState.WHITE_WINS
        elif cur_times[Player.WHITE.value] < 0:
            self.board.state = BoardState.BLACK_WINS

    def restart(self) -> None:
        """Перезапускает игру."""
        self.__init__()

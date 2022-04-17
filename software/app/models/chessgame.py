from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from datetime import date


class ChessFigure(Enum):
    bb, bk, bn, bp, bq, br, wb, wk, wn, wp, wq, wr, empty = range(13)


ChessPos = namedtuple('ChessPos', 'move_id, is_white_move, pos')


@dataclass
class Move(object):
    start_move: str
    end_move: str
    figure: ChessFigure
    move_number: int


@dataclass
class GamePlayer(object):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date


class ChessGame(object):
    class GameOutcome(Enum):
        white, black, draw = range(3)

    def __init__(self, begin_date: date, winner: GameOutcome, white_player, black_player, moves=None):
        if moves is None:
            moves = []

        self.positions = [[[ChessFigure.empty for _ in range(8)] for _ in range(8)]]
        self._moves = moves
        self._cur_pos = 0
        self._begin_date = begin_date
        self._winner = winner
        self.white_player = white_player
        self.black_player = black_player

    @property
    def moves(self) -> list[Move]:
        return self._moves

    def add_move(self, move: Move):
        self._moves.append(move)

    @property
    def cur_pos(self) -> int:
        return self._cur_pos

    @property
    def begin_date(self):
        return self._begin_date

    def fig(self, i, j) -> ChessFigure:
        return self.positions[self._cur_pos][i][j]

    def get_all_data(self):
        return self.positions, self._moves, self._begin_date, self._winner

    @classmethod
    def create_game_with_zero_moves(cls, begin_date: date = date.today(), winner: GameOutcome = GameOutcome.draw,
                                    white_player=None, black_player=None):
        chess_game = ChessGame(begin_date, winner, white_player, black_player)
        for col in range(8):
            chess_game.positions[chess_game.cur_pos][1][col] = ChessFigure.bp

        chess_game.positions[chess_game.cur_pos][0][0] = ChessFigure.br
        chess_game.positions[chess_game.cur_pos][0][1] = ChessFigure.bk
        chess_game.positions[chess_game.cur_pos][0][2] = ChessFigure.bb
        chess_game.positions[chess_game.cur_pos][0][3] = ChessFigure.bk
        chess_game.positions[chess_game.cur_pos][0][4] = ChessFigure.bq
        chess_game.positions[chess_game.cur_pos][0][5] = ChessFigure.bb
        chess_game.positions[chess_game.cur_pos][0][6] = ChessFigure.bk
        chess_game.positions[chess_game.cur_pos][0][7] = ChessFigure.br

        for col in range(8):
            chess_game.positions[chess_game.cur_pos][6][col] = ChessFigure.wp

        chess_game.positions[chess_game.cur_pos][7][0] = ChessFigure.wr
        chess_game.positions[chess_game.cur_pos][7][1] = ChessFigure.wk
        chess_game.positions[chess_game.cur_pos][7][2] = ChessFigure.wb
        chess_game.positions[chess_game.cur_pos][7][3] = ChessFigure.wk
        chess_game.positions[chess_game.cur_pos][7][4] = ChessFigure.wq
        chess_game.positions[chess_game.cur_pos][7][5] = ChessFigure.wb
        chess_game.positions[chess_game.cur_pos][7][6] = ChessFigure.wk
        chess_game.positions[chess_game.cur_pos][7][7] = ChessFigure.wr

        return chess_game

    @cur_pos.setter
    def cur_pos(self, value):
        self._cur_pos = value

import enum
import logging
from collections import namedtuple

import chess
from sqlalchemy import Enum, orm

from datetime import date

from sqlalchemy import Column, String, SmallInteger, ForeignKey, Integer, Date, MetaData
from sqlalchemy.orm import declarative_base, relationship


class ChessFigure(enum.IntEnum):
    bb, bk, bn, bp, bq, br, wb, wk, wn, wp, wq, wr, empty = range(13)


chess_figure_to_str = {
    ChessFigure.wp: '',
    ChessFigure.bp: '',
    ChessFigure.wr: 'R',
    ChessFigure.br: 'R',
    ChessFigure.wn: 'N',
    ChessFigure.bn: 'N',
    ChessFigure.wb: 'B',
    ChessFigure.bb: 'B',
    ChessFigure.wq: 'Q',
    ChessFigure.bq: 'Q',
    ChessFigure.wk: 'K',
    ChessFigure.bk: 'K'
}

ChessPos = namedtuple('ChessPos', 'move_id, is_white_move, pos')

metadata_obj = MetaData()
Base = declarative_base(metadata=metadata_obj)


class Move(Base):
    __tablename__ = 'move'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    start_move = Column('start_move', String(2), nullable=False)
    end_move = Column('end_move', String(2), nullable=False)
    meta = Column('meta', String(), nullable=False)
    figure = Column('figure', Enum(ChessFigure), nullable=False)
    move_number = Column('move_number', SmallInteger, nullable=False)
    chess_game = Column('chess_game', Integer, ForeignKey('chess_game.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, start_move: str, end_move: str, meta: str, figure: ChessFigure, move_number: int):
        self.start_move = start_move
        self.end_move = end_move
        self.meta = meta
        self.figure = figure
        self.move_number = move_number


class ChessPlayer(Base):
    __tablename__ = 'chess_player'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    date_of_birth = Column('date_of_birth', Date)
    comment = Column('comment', String, nullable=True)

    chess_games = relationship('AssociationChessPlayerChessGame', back_populates='chess_player')

    def __init__(self, first_name: str, last_name: str, date_of_birth: date, comment: str):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.comment = comment


class ChessGame(Base):
    class GameOutcome(enum.Enum):
        white, black, draw = range(3)

    __tablename__ = 'chess_game'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    begin_date = Column('begin_date', Date, nullable=True)
    winner = Column('winner', Enum(GameOutcome), nullable=False)

    chess_players = relationship('AssociationChessPlayerChessGame', back_populates='chess_game', cascade="all, delete")
    moves = relationship('Move', cascade="all, delete", lazy='selectin')

    def __init__(self, begin_date: date = date.today(), winner: GameOutcome = GameOutcome.draw,
                 white_player: ChessPlayer = None, black_player: ChessPlayer = None,
                 moves=None):
        if moves is None:
            moves = []
        self._positions = [[[ChessFigure.empty for _ in range(8)] for _ in range(8)]]
        self.moves = moves
        self._cur_pos = 0
        self.begin_date = begin_date
        self.winner = winner
        self.white_player = white_player
        self.black_player = black_player

        self._moves_to_positions()

    @orm.reconstructor
    def init_on_load(self):
        self._positions = [[[ChessFigure.empty for _ in range(8)] for _ in range(8)]]
        self._cur_pos = 0
        self._moves_to_positions()

    def add_move(self, move: Move):
        self.moves.append(move)

    def fig(self, i, j) -> ChessFigure:
        return self._positions[self._cur_pos][i][j]

    def cur_move_start(self):
        return self.moves[self.cur_pos - 1].start_move

    def cur_move_end(self):
        return self.moves[self.cur_pos - 1].end_move

    @classmethod
    def create_game_with_zero_moves(cls, begin_date: date = date.today(), winner: GameOutcome = GameOutcome.draw,
                                    white_player=None, black_player=None):
        chess_game = ChessGame(begin_date, winner, white_player, black_player, [])
        for col in range(8):
            chess_game._positions[chess_game.cur_pos][1][col] = ChessFigure.bp

        chess_game._positions[chess_game.cur_pos][0][0] = ChessFigure.br
        chess_game._positions[chess_game.cur_pos][0][1] = ChessFigure.bn
        chess_game._positions[chess_game.cur_pos][0][2] = ChessFigure.bb
        chess_game._positions[chess_game.cur_pos][0][3] = ChessFigure.bq
        chess_game._positions[chess_game.cur_pos][0][4] = ChessFigure.bk
        chess_game._positions[chess_game.cur_pos][0][5] = ChessFigure.bb
        chess_game._positions[chess_game.cur_pos][0][6] = ChessFigure.bn
        chess_game._positions[chess_game.cur_pos][0][7] = ChessFigure.br

        for col in range(8):
            chess_game._positions[chess_game.cur_pos][6][col] = ChessFigure.wp

        chess_game._positions[chess_game.cur_pos][7][0] = ChessFigure.wr
        chess_game._positions[chess_game.cur_pos][7][1] = ChessFigure.wn
        chess_game._positions[chess_game.cur_pos][7][2] = ChessFigure.wb
        chess_game._positions[chess_game.cur_pos][7][3] = ChessFigure.wq
        chess_game._positions[chess_game.cur_pos][7][4] = ChessFigure.wk
        chess_game._positions[chess_game.cur_pos][7][5] = ChessFigure.wb
        chess_game._positions[chess_game.cur_pos][7][6] = ChessFigure.wn
        chess_game._positions[chess_game.cur_pos][7][7] = ChessFigure.wr

        return chess_game

    @property
    def cur_pos(self):
        return self._cur_pos

    @cur_pos.setter
    def cur_pos(self, pos_no):
        if pos_no < 0:
            self._cur_pos = 0
        elif pos_no < self.positions_num:
            self._cur_pos = pos_no
        else:
            self._cur_pos = 0

    def _moves_to_positions(self):
        if not self.moves:
            return
        board = chess.Board()
        self._positions = [PosParser.parse(board.epd())]
        for move in self.moves:
            board.push_san(MoveStringifier.stringify(move))
            self._positions += [PosParser.parse(board.epd())]

    @property
    def positions_num(self):
        return len(self._positions)


class MoveStringifier:

    @staticmethod
    def stringify(move: Move):
        if move.meta.startswith('O-O'):
            return move.meta

        move_str = ''

        move_str += chess_figure_to_str[move.figure]

        if move.figure == ChessFigure.wr or move.figure == ChessFigure.br:
            if move.meta and move.meta[0] != 'x' and move.meta[0].isalnum():
                move_str += move.meta[0]

        if 'x' in move.meta:
            move_str += 'x'
            if move.figure == ChessFigure.wp or move.figure == ChessFigure.bp:
                move_str = move.start_move[0] + move_str
        move_str += move.end_move

        if '+' in move.meta:
            move_str += '+'

        return move_str


class PosParser(object):
    chess_to_chess_figure = {
        'b': ChessFigure.bb,
        'B': ChessFigure.wb,
        'k': ChessFigure.bk,
        'K': ChessFigure.wk,
        'n': ChessFigure.bn,
        'N': ChessFigure.wn,
        'p': ChessFigure.bp,
        'P': ChessFigure.wp,
        'q': ChessFigure.bq,
        'Q': ChessFigure.wq,
        'r': ChessFigure.br,
        'R': ChessFigure.wr
    }

    @staticmethod
    def letter_to_coords(s: str):
        first = ord(s[0]) - 97
        second = 7 - (int(s[1]) - 1)
        return second, first

    @staticmethod
    def to_chess_figure(chess) -> ChessFigure:
        return PosParser.chess_to_chess_figure[chess]

    @staticmethod
    def parse(pos_str: str):
        prefix = pos_str[0: pos_str.find(' ')]
        suffix = pos_str[pos_str.find(' '):]
        prefix = prefix.split('/')
        pos = [[ChessFigure.empty for _ in range(8)] for _ in range(8)]

        try:
            for row_no, row in enumerate(prefix):
                col_no = 0
                for i in range(len(row)):
                    if str.isdigit(row[i]):
                        col_no += int(row[i])
                    elif str.isalpha(row[i]):
                        pos[row_no][col_no] = PosParser.to_chess_figure(row[i])
                        col_no += 1
                    else:
                        raise Exception('symbol must be digit or alpha')

        except Exception as e:
            logging.critical(f'Failed to parse position: {e}')
            return [[ChessFigure.empty for _ in range(8)] for _ in range(8)]

        return pos


class AssociationChessPlayerChessGame(Base):
    class Color(enum.Enum):
        white, black = range(2)

    __tablename__ = 'chess_player_chess_game'

    chess_player_id = Column('chess_player_id', ForeignKey('chess_player.id'), primary_key=True)
    chess_game_id = Column('chess_game_id', ForeignKey('chess_game.id'), primary_key=True)
    color = Column('color', Enum(Color), nullable=False)

    chess_player = relationship("ChessPlayer", back_populates="chess_games")
    chess_game = relationship("ChessGame", back_populates="chess_players")

import enum
from collections import namedtuple
from sqlalchemy import Enum

from datetime import date

from sqlalchemy import Column, String, SmallInteger, ForeignKey, Integer, Date, MetaData
from sqlalchemy.orm import declarative_base, relationship


class ChessFigure(enum.Enum):
    bb, bk, bn, bp, bq, br, wb, wk, wn, wp, wq, wr, empty = range(13)


ChessPos = namedtuple('ChessPos', 'move_id, is_white_move, pos')

metadata_obj = MetaData()
Base = declarative_base(metadata=metadata_obj)


class Move(Base):
    __tablename__ = 'move'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    start_move = Column('start_move', String(2), nullable=False)
    end_move = Column('end_move', String(2), nullable=False)
    figure = Column('figure', Enum(ChessFigure), nullable=False)
    move_number = Column('move_number', SmallInteger, nullable=False)
    chess_game = Column('chess_game', Integer, ForeignKey('chess_game.id'))

    def __init__(self, start_move: str, end_move: str, figure: ChessFigure, move_number: int):
        self.start_move = start_move
        self.end_move = end_move
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
    begin_date = Column('begin_date', Date, nullable=False)
    winner = Column('winner', Enum(GameOutcome), nullable=False)

    chess_players = relationship('AssociationChessPlayerChessGame', back_populates='chess_game')
    moves = relationship('Move')

    def __init__(self, begin_date: date, winner: GameOutcome, white_player: ChessPlayer, black_player: ChessPlayer,
                 moves=None):
        if moves is None:
            moves = []

        self.positions = [[[ChessFigure.empty for _ in range(8)] for _ in range(8)]]
        self._moves = moves
        self._cur_pos = 0
        self.begin_date = begin_date
        self.winner = winner
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

    def fig(self, i, j) -> ChessFigure:
        return self.positions[self._cur_pos][i][j]

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


class AssociationChessPlayerChessGame(Base):
    class Color(enum.Enum):
        white, black = range(2)

    __tablename__ = 'chess_player_chess_game'

    chess_player_id = Column('chess_player_id', ForeignKey('chess_player.id'), primary_key=True)
    chess_game_id = Column('chess_game_id', ForeignKey('chess_game.id'), primary_key=True)
    color = Column('color', Enum(Color), nullable=False)

    chess_player = relationship("ChessPlayer", back_populates="chess_games")
    chess_game = relationship("ChessGame", back_populates="chess_players")
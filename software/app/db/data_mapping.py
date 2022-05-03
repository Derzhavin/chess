from sqlalchemy.orm import registry
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import SmallInteger
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from sqlalchemy import Column, create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import registry

from app.models import ChessGame, Move, GamePlayer, ChessFigure

mapper_registry = registry()
metadata_obj = MetaData()

move_table = Table(
    'move',
    metadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('start_move', String(2), nullable=False),
    Column('end_move', String(2), nullable=False),
    Column('figure', Enum(ChessFigure), nullable=False),
    Column('move_number', SmallInteger, nullable=False),
    Column('chess_game', BigInteger, ForeignKey('chess_game.id')),
)

chess_game_table = Table(
    'chess_game',
    metadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('begin_date', Date, nullable=False),
    Column('winner', Enum(ChessGame.GameOutcome), nullable=False),
    Column('white_player', BigInteger, ForeignKey('chess_player.id'), nullable=True),
    Column('black_player', BigInteger, ForeignKey('chess_player.id'), nullable=True),
)

chess_player_table = Table(
    'chess_player',
    metadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('date_of_birth', Date),
    Column('comment', String, nullable=True)
)

mapper_registry.map_imperatively(ChessGame, chess_game_table, properties={
    'moves': relationship(Move),
})

mapper_registry.map_imperatively(Move, move_table)
mapper_registry.map_imperatively(GamePlayer, chess_player_table)
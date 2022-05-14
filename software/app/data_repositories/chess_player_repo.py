from .repo_interfaces import IGamePlayerRepo
from sqlalchemy.orm import Session
from app.store import ChessPlayer


class ChessPlayerRepo(IGamePlayerRepo):

    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def add_player(self, game_player: ChessPlayer):
        self.__db_session.add(game_player)

    def get_players(self, criterion):
        return self.__db_session.query(ChessPlayer).where(criterion).all()

    def get_player_by_id(self, game_player_id: int):
        return self.__db_session.query(ChessPlayer).where(ChessPlayer.id == game_player_id).one()

    def exists(self, criterion):
        q = self.__db_session.query(ChessPlayer).filter(criterion)
        existence = self.__db_session.query(q.exists()).scalar()
        return existence

    def count(self, criterion):
        return self.__db_session.query(ChessPlayer).filter(criterion).count()

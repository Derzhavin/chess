from .repo_interfaces import IGamePlayerRepo
from sqlalchemy.orm import Session
from app.models import GamePlayer


class GamePlayerRepo(IGamePlayerRepo):

    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def add(self, game_player: GamePlayer):
        self.__db_session.add(game_player)

    def get(self, criterion):
        return self.__db_session.query(GamePlayer).where(criterion)

    def exists(self, criterion):
        q = self.__db_session.query(GamePlayer).filter(criterion)
        return self.__db_session.query(q.exists())

    def count(self, criterion):
        return self.__db_session.query(GamePlayer).filter(criterion).count()

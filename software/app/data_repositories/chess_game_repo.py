from .repo_interfaces import IChessGameRepo
from app.models import ChessGame
from sqlalchemy.orm import Session


class ChessGameRepo(IChessGameRepo):

    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def add(self, chess_game: ChessGame):
        self.__db_session.add(chess_game)

    def get(self, chess_game_id):
        return self.__db_session.query(ChessGame).where(ChessGame.id == chess_game_id)

from .repo_interfaces import IChessGameRepo
from app.store import ChessGame, AssociationChessPlayerChessGame
from sqlalchemy.orm import Session


class ChessGameRepo(IChessGameRepo):

    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def add_game(self, chess_game: ChessGame):
        white = AssociationChessPlayerChessGame(color=AssociationChessPlayerChessGame.Color.white)
        white.chess_player = chess_game.white_player
        chess_game.chess_players.append(white)

        black = AssociationChessPlayerChessGame(color=AssociationChessPlayerChessGame.Color.black)
        black.chess_player = chess_game.black_player
        chess_game.chess_players.append(black)

        self.__db_session.add(chess_game)

    def get_game_by_id(self, chess_game_id: int):
        return self.__db_session.query(ChessGame).where(ChessGame.id == chess_game_id).one()

    def get_games(self, criterion):
        return self.__db_session.query(ChessGame).where(criterion).all()

    def delete_game(self, criterion):
        chess_game = self.__db_session.query(ChessGame).filter(criterion).first()
        self.__db_session.delete(chess_game)

    def count(self, criterion):
        return self.__db_session.query(ChessGame).filter(criterion).count()
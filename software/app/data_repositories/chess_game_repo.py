from sqlalchemy import and_, or_

from .repo_interfaces import IChessGameRepo
from app.store import ChessGame, ChessPlayer, AssociationChessPlayerChessGame
from sqlalchemy.orm import Session
from datetime import date


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
        return self.__db_session.query(ChessGame).filter(criterion).all()

    def delete_game(self, criterion):
        chess_game = self.__db_session.query(ChessGame).filter(criterion).first()
        self.__db_session.delete(chess_game)

    def count(self, criterion):
        return self.__db_session.query(ChessGame).filter(criterion).count()

    def get_games_super_query(self, begin_date: date=None, white_player_first_name_pattern=None,
                              white_player_last_name_pattern=None,
                              black_player_first_name_pattern=None, black_player_last_name_pattern=None):
        criterion_data = []
        if begin_date:
            criterion_data += [and_(True, ChessGame.begin_date == begin_date)]

        white_player_criterion_data = []
        if white_player_first_name_pattern:
            white_player_criterion_data += [and_(ChessPlayer.first_name.like(white_player_first_name_pattern),
                                AssociationChessPlayerChessGame.color == AssociationChessPlayerChessGame.Color.white)]

        if white_player_last_name_pattern:
            white_player_criterion_data += [and_(ChessPlayer.last_name.like(white_player_last_name_pattern),
                                AssociationChessPlayerChessGame.color == AssociationChessPlayerChessGame.Color.white)]

        black_player_criterion_data = []
        if black_player_first_name_pattern:
            black_player_criterion_data += [and_(ChessPlayer.first_name.like(black_player_first_name_pattern),
                                    AssociationChessPlayerChessGame.color == AssociationChessPlayerChessGame.Color.black)]

        if black_player_last_name_pattern:
            black_player_criterion_data += [and_(ChessPlayer.last_name.like(black_player_last_name_pattern),
                                    AssociationChessPlayerChessGame.color == AssociationChessPlayerChessGame.Color.black)]

        if white_player_criterion_data and black_player_criterion_data:
            criterion_data += [or_(and_(*white_player_criterion_data), and_(*black_player_criterion_data))]
        elif white_player_criterion_data:
            criterion_data += [and_(True, *white_player_criterion_data)]
        elif black_player_criterion_data:
            criterion_data += [and_(True, *black_player_criterion_data)]

        criterion = True if not criterion_data else and_(*criterion_data)

        query = self.__db_session \
            .query(ChessGame) \
            .join(AssociationChessPlayerChessGame) \
            .join(ChessPlayer) \
            .filter(criterion)
        print(str(query))
        return query.all()

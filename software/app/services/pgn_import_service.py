from typing import Callable

from PyQt5.QtWidgets import QMessageBox, QWidget
from app.data_repositories import IChessGameRepo, IGamePlayerRepo
from sqlalchemy.orm import Session

from software.app.parsers import ChessGamePgnParser
from software.app.models import ChessGame, GamePlayer
from software.app.presenters import GamePlayerResolveDialog

from sqlalchemy import and_
from typing import TypeVar, Generic


class PgnImportService(Generic[IChessGameRepo, IGamePlayerRepo]):

    def __init__(self, session: Session):
        self.session = session
        self.chess_game_repo = IChessGameRepo(session)
        self.game_player_repo = IGamePlayerRepo(session)

    def load_game_from_pgn(self, pgn_path: str, parent_widget: QWidget, config) -> bool:
        pgn_parser = ChessGamePgnParser(pgn_path)
        pgn_parser.load_first_game()

        if not pgn_parser.valid:
            return False

        first_name, last_name = pgn_parser.white_player
        criterion = and_(GamePlayer.first_name == first_name, GamePlayer.first_name == last_name)

        self.session.begin()

        if self.game_player_repo.exists(criterion):
            if not GamePlayerResolveDialog(parent_widget, config).exec():
                pass
            else:
                pass
        else:
            white_player = GamePlayer(first_name, last_name, None, '')

        first_name, last_name = pgn_parser.black_player
        criterion = and_(GamePlayer.first_name == first_name, GamePlayer.first_name == last_name)

        if self.game_player_repo.exists(criterion):
            pass
        else:
            black_player = GamePlayer(first_name, last_name, None, '')

        chess_game = ChessGame(pgn_parser.begin_date, pgn_parser.game_outcome, white_player, black_player, pgn_parser.moves)

        self.chess_game_repo.add(chess_game)
        return True

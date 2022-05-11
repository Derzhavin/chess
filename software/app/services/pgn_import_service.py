from PyQt5.QtWidgets import QMessageBox, QWidget
from sqlalchemy.orm import Session, sessionmaker

from app.parsers import ChessGamePgnParser
from app.store import ChessGame, ChessPlayer
from app.presenters import GamePlayerResolveDialog

from sqlalchemy import and_
from typing import TypeVar, Generic

ChessGameRepoT = TypeVar('ChessGameRepoT')
ChessPlayerRepoT = TypeVar('ChessPlayerRepoT')


class PgnImportService:

    def __init__(self, engine, chess_game_repo_cls: ChessGameRepoT, game_player_repo_cls: ChessPlayerRepoT):
        self.session = sessionmaker(engine)()
        self.chess_game_repo = chess_game_repo_cls(self.session)
        self.game_player_repo = game_player_repo_cls(self.session)

    def load_game_from_pgn(self, pgn_path: str, parent_widget: QWidget, config) -> bool:
        pgn_parser = ChessGamePgnParser(pgn_path)
        pgn_parser.load_first_game()

        if not pgn_parser.valid:
            return False

        self.session.begin()

        first_name, last_name = pgn_parser.white_player
        criterion = and_(ChessPlayer.first_name == first_name, ChessPlayer.last_name == last_name)

        if self.game_player_repo.exists(criterion):
            if not GamePlayerResolveDialog(parent_widget, config, self.game_player_repo, criterion).exec():
                self.session.rollback()
                return False
            else:
                pass
        else:
            white_player = ChessPlayer(first_name, last_name, None, '')
            self.game_player_repo.add_player(white_player)

        first_name, last_name = pgn_parser.black_player
        criterion = and_(ChessPlayer.first_name == first_name, ChessPlayer.last_name == last_name)

        if self.game_player_repo.exists(criterion):
            if not GamePlayerResolveDialog(parent_widget, config, self.game_player_repo).exec():
                self.session.rollback()
                return False
        else:
            black_player = ChessPlayer(first_name, last_name, None, '')
            self.game_player_repo.add_player(black_player)

        chess_game = ChessGame(
            pgn_parser.begin_date,
            pgn_parser.game_outcome,
            white_player, black_player,
            pgn_parser.moves)

        self.chess_game_repo.add_game(chess_game)

        self.session.commit()

        return True

    def __del__(self):
        self.session.close()
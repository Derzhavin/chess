from PyQt5.QtWidgets import QMessageBox, QWidget
from sqlalchemy.orm import Session, sessionmaker

from app.parsers import ChessGamePgnParser
from app.store import ChessGame, ChessPlayer
from app.presenters import GamePlayerResolveDialog

from sqlalchemy import and_


class PgnImportService:

    def __init__(self, engine, chess_game_repo_cls, game_player_repo_cls):
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
            game_player_resolve_dialog = GamePlayerResolveDialog(parent_widget, config, self.game_player_repo, criterion)
            if not game_player_resolve_dialog.exec():
                self.session.rollback()
                return False
            else:
                if game_player_resolve_dialog.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
                    pass
                elif game_player_resolve_dialog.selected_option ==  GamePlayerResolveDialog.SelectedOptionStep.create_player_op:
                    white_player = ChessPlayer(
                        game_player_resolve_dialog.target_chess_player_first_name,
                        game_player_resolve_dialog.target_chess_player_last_name,
                        game_player_resolve_dialog.target_chess_player_date_of_birth,
                        game_player_resolve_dialog.target_chess_player_comment
                    )
        else:
            white_player = ChessPlayer(first_name, last_name, None, '')
            self.game_player_repo.add_player(white_player)

        first_name, last_name = pgn_parser.black_player
        criterion = and_(ChessPlayer.first_name == first_name, ChessPlayer.last_name == last_name)

        if self.game_player_repo.exists(criterion):
            game_player_resolve_dialog = GamePlayerResolveDialog(parent_widget, config, self.game_player_repo, criterion)
            if not game_player_resolve_dialog.exec():
                self.session.rollback()
                return False
            else:
                if game_player_resolve_dialog.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
                    pass
                elif game_player_resolve_dialog.selected_option == GamePlayerResolveDialog.SelectedOptionStep.create_player_op:
                    black_player = ChessPlayer(
                        game_player_resolve_dialog.target_chess_player_first_name,
                        game_player_resolve_dialog.target_chess_player_last_name,
                        game_player_resolve_dialog.target_chess_player_date_of_birth,
                        game_player_resolve_dialog.target_chess_player_comment
                    )
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
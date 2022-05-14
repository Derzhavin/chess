from PyQt5.QtWidgets import QMessageBox, QWidget
from sqlalchemy.orm import sessionmaker

from app.parsers import ChessGamePgnParser
from app.store import ChessGame, ChessPlayer
from app.presenters import ChessPlayerResolveDialog

from sqlalchemy import and_


class PgnImportService:

    def __init__(self, engine, chess_game_repo_cls, chess_player_repo_cls):
        self.session = sessionmaker(engine)()
        self.chess_game_repo = chess_game_repo_cls(self.session)
        self.chess_player_repo = chess_player_repo_cls(self.session)

    def load_game_from_pgn(self, pgn_path: str, parent_widget: QWidget, config):
        pgn_parser = ChessGamePgnParser(pgn_path)
        pgn_parser.load_first_game()

        if not pgn_parser.valid:
            return False

        self.session.begin()

        first_name, last_name = pgn_parser.white_player
        criterion = and_(ChessPlayer.first_name == first_name, ChessPlayer.last_name == last_name)

        if self.chess_player_repo.exists(criterion):
            chess_player_resolve_dialog = ChessPlayerResolveDialog(
                parent_widget,
                config,
                self.chess_player_repo,
                criterion,
                first_name,
                last_name
            )
            if not chess_player_resolve_dialog.exec() \
                    or chess_player_resolve_dialog.selected_option == ChessPlayerResolveDialog.SelectedOptionStep.cancel_op:
                QMessageBox.information(parent_widget, 'Импорт партии', 'Импорт партии из pgn был отменён')
                self.session.rollback()
                return
            elif chess_player_resolve_dialog.selected_option == ChessPlayerResolveDialog.SelectedOptionStep.choose_player_op:
                white_player = self.chess_player_repo.get_player_by_id(chess_player_resolve_dialog.target_chess_player_id)
            elif chess_player_resolve_dialog.selected_option ==  ChessPlayerResolveDialog.SelectedOptionStep.create_player_op:
                white_player = ChessPlayer(
                    first_name,
                    last_name,
                    chess_player_resolve_dialog.target_chess_player_date_of_birth,
                    chess_player_resolve_dialog.target_chess_player_comment
                )
                self.chess_player_repo.add_player(white_player)
        else:
            white_player = ChessPlayer(first_name, last_name, None, '')
            self.chess_player_repo.add_player(white_player)

        first_name, last_name = pgn_parser.black_player
        criterion = and_(ChessPlayer.first_name == first_name, ChessPlayer.last_name == last_name)

        if self.chess_player_repo.exists(criterion):
            chess_player_resolve_dialog = ChessPlayerResolveDialog(
                parent_widget,
                config,
                self.chess_player_repo,
                criterion,
                first_name,
                last_name
            )

            if not chess_player_resolve_dialog.exec() \
                or chess_player_resolve_dialog.selected_option == ChessPlayerResolveDialog.SelectedOptionStep.cancel_op:
                QMessageBox.information(parent_widget, 'Импорт партии', 'Импорт партии из pgn был отменён')
                self.session.rollback()
                return
            elif chess_player_resolve_dialog.selected_option == ChessPlayerResolveDialog.SelectedOptionStep.choose_player_op:
                black_player = self.chess_player_repo.get_player_by_id(chess_player_resolve_dialog.target_chess_player_id)
            elif chess_player_resolve_dialog.selected_option == ChessPlayerResolveDialog.SelectedOptionStep.create_player_op:
                black_player = ChessPlayer(
                    first_name,
                    last_name,
                    chess_player_resolve_dialog.target_chess_player_date_of_birth,
                    chess_player_resolve_dialog.target_chess_player_comment
                )
                self.chess_player_repo.add_player(black_player)
        else:
            black_player = ChessPlayer(first_name, last_name, None, '')
            self.chess_player_repo.add_player(black_player)

        chess_game = ChessGame(
            pgn_parser.begin_date,
            pgn_parser.game_outcome,
            white_player, black_player,
            pgn_parser.moves)

        self.chess_game_repo.add_game(chess_game)

        self.session.commit()

        QMessageBox.information(parent_widget, 'Информация', 'Партия была успешно импортирована')

    def __del__(self):
        self.session.close()
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from app.views.chessboard import ChessBoardView
from app.controllers.game_controllers import GameController
from app.data_repositories import ChessGameRepo, ChessPlayerRepo
from app.services import PgnImportService, ChessGameDeleteService


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, engine, config):
        super().__init__()
        uic.loadUi(config.main_window_ui_path, self)
        self.config = config
        self.board_graphics_view.setBackgroundBrush(QColor(config.chessboard_view_background_color))
        self.board_graphics_view.zoom_in_factor = config.chessboard_zoom_in_factor
        self._chessboard_view = ChessBoardView(self.board_graphics_view, config)

        self._game_controller = GameController(self._chessboard_view)
        self._game_controller.represent_postion()
        self.engine = engine
        self.import_game_action.triggered.connect(self.on_game_import_triggered)
        self.action_delete_game.triggered.connect(self.on_game_delete_triggered)

    def on_game_import_triggered(self):
        file_dialog  = QFileDialog(self)
        file_dialog.setNameFilter("Game (*.pgn)")
        file_dialog.setWindowTitle("Импорт игры")

        if file_dialog.exec():
            pgn_path = file_dialog.selectedFiles()[0]
            pgn_import_service = PgnImportService(self.engine, ChessGameRepo, ChessPlayerRepo)
            pgn_import_service.load_game_from_pgn(pgn_path, self, self.config)

    def on_game_delete_triggered(self):
        chess_game_delete_service = ChessGameDeleteService(self.config, self, self.engine, ChessGameRepo)
        chess_game_delete_service.delete_game()

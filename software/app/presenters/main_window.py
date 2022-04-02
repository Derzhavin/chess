import logging
from datetime import date

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QColor

from app.views.chessboard import ChessBoardView

from app.controllers.game_controllers import GameController

from app.models import ChessGame, GamePlayer


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, config):
        super().__init__()
        uic.loadUi(config.main_window_ui_path, self)
        self.config = config
        self.board_graphics_view.setBackgroundBrush(QColor(config.chessboard_view_background_color))
        self.board_graphics_view.zoom_in_factor = config.chessboard_zoom_in_factor
        self._chessboard_view = ChessBoardView(self.board_graphics_view, config)

        white_player = GamePlayer('Billy', 'Jones', '1990')
        black_player = GamePlayer('Jonny', 'Jones', '1990')
        chess_game = ChessGame.create_game_with_zero_moves(date.today(), ChessGame.GameOutcome.white, white_player, black_player)
        self._game_controller = GameController(self._chessboard_view, chess_game)
        self._game_controller.represent_common_starting_postion()

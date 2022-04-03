from PyQt5.QtCore import QObject

from .data_repositories.chess_game_repo import ChessGameRepo
from .factories import AssetsFactory
from .presenters import MainWindow
import logging


class App(QObject):

    def __init__(self, config):
        super().__init__()
        self.config = config

        logging.basicConfig(
            filename=config.log_file,
            level=config.log_level,
            filemode='w',
            format='%(name)s - %(levelname)s - %(message)s'
        )

        AssetsFactory(config)

        chess_game_repo = chess_game_repo = ChessGameRepo()

        self.main_window = MainWindow(chess_game_repo, config)

    def start(self):
        self.main_window.show()
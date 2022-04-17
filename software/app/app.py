from PyQt5.QtCore import QObject
from sqlalchemy.orm import sessionmaker

from .data_repositories.chess_game_repo import ChessGameRepo
from .assets_factory import AssetsFactory
from .presenters import MainWindow
from .db import init_engine

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

        engine = init_engine(config.db_uri)
        session = sessionmaker(bind=engine)()
        chess_game_repo = ChessGameRepo(session)

        self.main_window = MainWindow(chess_game_repo, config)

    def start(self):
        self.main_window.show()
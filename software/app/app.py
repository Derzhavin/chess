from PyQt5.QtCore import QObject

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

        self.main_window = MainWindow(engine, config)

    def start(self):
        self.main_window.show()
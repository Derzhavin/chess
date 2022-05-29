from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMovie


class WaitAnimationDialog(QtWidgets.QDialog):

    def __init__(self, parent, config):
        super().__init__(parent)
        uic.loadUi(config.wait_dialog_ui_path, self)

        self.movie = QMovie(config.wait_gif_path)
        self.label_wait_movie.setMovie(self.movie)
        self.movie.start()

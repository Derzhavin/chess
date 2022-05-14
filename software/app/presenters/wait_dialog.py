from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMovie
from app.assets_factory import AssetsFactory


class WaitDialog(QtWidgets.QDialog):

    def __init__(self, parent, config):
        super().__init__(parent)
        uic.loadUi(config.wait_dialog_ui_path, self)

        self.movie = QMovie(config.wait_gif_path)
        self.label_wait_movie.setMovie(self.movie)
        self.movie.start()
        self.push_button_ok.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.reject)

    @pyqtSlot()
    def on_completed(self):
        self.movie.stop()
        self.label_wait_movie.setPixmap(AssetsFactory().checked_pixmap)
        self.push_button_ok.setEnabled(True)
        self.push_button_cancel.setEnabled(False)

    @property
    def info(self):
        return self.label_info.text()

    @info.setter
    def info(self, msg: str):
        self.label_info.setText(msg)

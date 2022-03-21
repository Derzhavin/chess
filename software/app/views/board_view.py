from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsView


class BoardView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zoom_in_factor = 1

    @property
    def zoom_in_factor(self) -> float:
        return self._zoom_in_factor

    @zoom_in_factor.setter
    def zoom_in_factor(self, factor: float):
        self._zoom_in_factor = factor

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(1 / self.zoom_in_factor, 1 / self.zoom_in_factor)


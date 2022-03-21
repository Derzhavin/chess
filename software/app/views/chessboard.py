from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from app.models import ChessFigure
from app.factories import AssetsFactory


class ChessBoardView(QObject):

    def __init__(self, view: QGraphicsView, config):
        super().__init__()
        self.view = view
        self.scene = QGraphicsScene()
        self.chessboard = Chessboard(config)
        self.scene.addItem(self.chessboard)
        self.view.setScene(self.scene)


class Piece(QGraphicsPixmapItem):

    def __init__(self, fig: ChessFigure, i: int, j: int, parent):
        super().__init__(parent)
        self.setPixmap(AssetsFactory().figure_pixmap[fig])
        self._fig = fig
        self.i = i
        self.j = j


class Chessboard(QGraphicsRectItem):

    def __init__(self, config):
        super().__init__(config.chessboard_x, config.chessboard_y, config.chessboard_size, config.chessboard_size)
        self._cell_size = config.chessboard_size / 8
        self._cells = []
        self._pieces = []

        for i in range(8):
            row = []
            for j in range(8):
                x = config.chessboard_x + j * self._cell_size
                y = config.chessboard_y + i * self._cell_size
                if i % 2 == j % 2:
                    cell = Cell(x, y, self._cell_size, self,
                                config.chessboard_default_white_cell_color,
                                config.chessboard_highlight_white_cell_color)
                else:
                    cell = Cell(x, y, self._cell_size, self,
                                config.chessboard_default_black_cell_color,
                                config.chessboard_highlight_black_cell_color)

                row.append(cell)
            self._cells.append(row)

    def cell(self, i: int, j: int):
        return self._cells[j][i]

    def put_piece(self, fig: ChessFigure, i: int, j: int):
        piece = Piece(fig, i, j, self)
        x = self.x() + j * self._cell_size
        y = self.y() + i * self._cell_size
        piece.setPos(x, y)
        piece.setVisible(True)
        piece.setZValue(1)
        self.scene().addItem(piece)
        self._pieces.append(piece)

    def piece(self, i: int, j: int):
        pieces = list(filter(lambda fig: fig.i == i and fig.j == j, self._pieces))
        if pieces:
            return pieces[0]
        return None

    def remove_piece(self, piece: Piece):
        self.scene().removeItem(piece)
        self._pieces.remove(piece)

    def remove_all_pieces(self):
        i = len(self._pieces)
        while i > 0:
            self.remove_piece(self._pieces[i - 1])
            i -= 1


class Cell(QGraphicsRectItem):

    def __init__(self, x: int, y: int, size: int, parent: Chessboard, default_color: str = '#F0D9B5',
                 highlight_color: str = '#F7EC74'):
        super().__init__(x, y, size, size, parent)
        self._default_color = QColor(default_color)
        self._highlight_color = QColor(highlight_color)
        self.setBrush(self._default_color)

    def highlight_on(self):
        self.setBrush(self._highlight_color)

    def highlight_off(self):
        self.setBrush(self._default_color)

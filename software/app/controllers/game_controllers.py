from app.models import ChessGame, ChessFigure
from app.views import ChessBoardView


class GameController(object):

    def __init__(self, view: ChessBoardView, game: ChessGame):
        super().__init__()
        self._game_on = False
        self._game = game
        self._view = view

    def represent_common_starting_postion(self):
        for i in range(8):
            for j in range(8):
                fig = self._game.fig(i, j)
                if fig != ChessFigure.empty:
                    self._view.chessboard.put_piece(fig, i, j)
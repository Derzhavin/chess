from PyQt5.QtCore import pyqtSignal, QObject
from app.store import ChessGame, ChessFigure, PosParser
from app.views import ChessBoardView
import chess


class GameController(QObject):
    game_returned_to_begin_sig = pyqtSignal()
    game_finished_sig = pyqtSignal()
    game_started_sig = pyqtSignal()
    game_next_move_sig = pyqtSignal()

    def __init__(self, view: ChessBoardView, game: ChessGame = ChessGame.create_game_with_zero_moves()):
        super().__init__()
        self._game_on = False
        self._game = game
        self._view = view

    @property
    def game_on(self) -> bool:
        return self._game_on

    @game_on.setter
    def game_on(self, game_on: bool):
        self._game_on = game_on
        if self.game_on:
            self.do_next_move()

    @property
    def game(self) -> ChessGame:
        return self._game

    @game.setter
    def game(self, game: ChessGame):
        self._game = game
        self.represent_position()

    def do_next_move(self):
        if self._game.cur_pos == 0:
            self.game_started_sig.emit()

        self._game.cur_pos += 1

        if self._game.cur_pos == 0:
            for i in range(8):
                for j in range(8):
                    self._view.chessboard.cell(i, j).highlight_off()

            self.game_on = False
            self.game_finished_sig.emit()
        else:
            self.represent_position()
            self.game_next_move_sig.emit()

    def do_prev_move(self):
        self._game.cur_pos -= 1
        self.represent_position()

        if self._game.cur_pos == 0:
            self.game_on = False
            self.game_returned_to_begin_sig.emit()

    def to_begin(self):
        self.represent_position()
        self.game_on = False
        self.game_returned_to_begin_sig.emit()

    def to_end(self):
        self.game.cur_pos = self.game.positions_num - 1
        self.represent_position()

    def represent_position(self):
        self._view.chessboard.remove_all_pieces()

        for i in range(8):
            for j in range(8):
                fig = self.game.fig(i, j)
                if fig != ChessFigure.empty:
                    self._view.chessboard.put_piece(fig, i, j)

        for i in range(8):
            for j in range(8):
                self._view.chessboard.cell(i, j).highlight_off()

        if self._game.cur_pos != 0:

            start_str = self.game.cur_move_start()
            end_str = self.game.cur_move_end()
            start_y, start_x = PosParser.letter_to_coords(start_str)
            end_y, end_x = PosParser.letter_to_coords(end_str)

            self._view.chessboard.cell(start_x, start_y).highlight_on()
            self._view.chessboard.cell(end_x, end_y).highlight_on()
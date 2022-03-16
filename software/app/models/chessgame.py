from collections import namedtuple
import logging
import chess.pgn
import io

ChessFigure = namedtuple('ChessFigure', 'bb, bk, bn, bp, bq, br, wb, wk, wn, wp, wq, wr, empty')
ChessPos = namedtuple('ChessPos', 'move_id, is_white_move, pos')


class ChessGame(object):
    def __init__(self):
        self.positions = [[[ChessFigure.empty for _ in range(8)] for _ in range(8)]]
        self._cur_pos = 0

    @property
    def cur_pos(self):
        return self._cur_pos

    def fig(self, i, j) -> ChessFigure:
        return self.positions[self._cur_pos][i][j]

    @classmethod
    def create_game_with_zero_moves(cls):
        chess_game = ChessGame()
        for col in range(8):
            chess_game.positions[chess_game.cur_pos][1][col] = ChessFigure.bp

        chess_game.positions[chess_game.cur_pos][0][0] = ChessFigure.br
        chess_game.positions[chess_game.cur_pos][0][1] = ChessFigure.bk
        chess_game.positions[chess_game.cur_pos][0][2] = ChessFigure.bb
        chess_game.positions[chess_game.cur_pos][0][3] = ChessFigure.bk
        chess_game.positions[chess_game.cur_pos][0][4] = ChessFigure.bq
        chess_game.positions[chess_game.cur_pos][0][5] = ChessFigure.bb
        chess_game.positions[chess_game.cur_pos][0][6] = ChessFigure.bk
        chess_game.positions[chess_game.cur_pos][0][7] = ChessFigure.br

        for col in range(8):
            chess_game.positions[chess_game.cur_pos][6][col] = ChessFigure.wp


        chess_game.positions[chess_game.cur_pos][7][0] = ChessFigure.wr
        chess_game.positions[chess_game.cur_pos][7][1] = ChessFigure.wk
        chess_game.positions[chess_game.cur_pos][7][2] = ChessFigure.wb
        chess_game.positions[chess_game.cur_pos][7][3] = ChessFigure.wk
        chess_game.positions[chess_game.cur_pos][7][4] = ChessFigure.wq
        chess_game.positions[chess_game.cur_pos][7][5] = ChessFigure.wb
        chess_game.positions[chess_game.cur_pos][7][6] = ChessFigure.wk
        chess_game.positions[chess_game.cur_pos][7][7] = ChessFigure.wr

        return chess_game

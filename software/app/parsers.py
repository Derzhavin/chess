from datetime import date

from app.models import ChessGame, ChessFigure, Move, GamePlayer

import chess.pgn


class ChessGamePgnParser:

    def __init__(self, pgn_path: str):
        self.valid = False
        self.pgn_path = pgn_path
        self.black_player = ['', '']
        self.white_player = ['', '']
        self.begin_date = date.today()
        self.game_outcome = ChessGame.GameOutcome.draw
        self.moves = []

    def load_first_game(self):
        self.valid = False

        pgn = open(self.pgn_path)
        first_game = chess.pgn.read_game(pgn)

        self.white_player = first_game.headers['White'].split(',')
        self.black_player = first_game.headers['Black'].split(',')
        self.begin_date = date.fromisoformat(first_game.headers['Date'].replace('.', '-'))

        parsed_game_outcome = first_game.headers['Result']

        if parsed_game_outcome == '1-0':
            self.game_outcome = ChessGame.GameOutcome.white
        elif parsed_game_outcome == '0-1':
            self.game_outcome = ChessGame.GameOutcome.black
        elif parsed_game_outcome == '1/2-1/2':
            self.game_outcome = ChessGame.GameOutcome.draw
        else:
            return

        board = first_game.board()
        for i, move in enumerate(first_game.mainline_moves()):
            move_str = str(move)
            move_begin = move_str[:2]
            move_end = move_str[2:]
            san = board.san(move)

            chess_figure = ChessFigure.wp
            if len(san) == 2:
                chess_figure = ChessFigure.wp if board.turn == chess.WHITE else ChessFigure.bp
            elif san[0] == 'R':
                chess_figure = ChessFigure.wr if board.turn == chess.WHITE else ChessFigure.br
            elif san[0] == 'N':
                chess_figure = ChessFigure.wn if board.turn == chess.WHITE else ChessFigure.bn
            elif san[0] == 'B':
                chess_figure = ChessFigure.wb if board.turn == chess.WHITE else ChessFigure.bb
            elif san[0] == 'Q':
                chess_figure = ChessFigure.wb if board.turn == chess.WHITE else ChessFigure.wb
            elif san[0] == 'K':
                chess_figure = ChessFigure.wk if board.turn == chess.WHITE else ChessFigure.bk

            chess_move = Move(chess_figure, move_begin, move_end, i)
            self.moves.append(chess_move)
            board.push(move)

        self.valid = True
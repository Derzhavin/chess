from sqlalchemy.orm import Session

from app.store import ChessGame


class ChessGameLoadService:

    def __init__(self, engine, chess_game_repo_cls):
        self.engine = engine
        self.chess_game_repo_cls = chess_game_repo_cls

    def load_game(self, chess_game_id: int) -> ChessGame:
        with Session(self.engine) as session:
            chess_game_repo = self.chess_game_repo_cls(session)
            chess_game = chess_game_repo.get_game_by_id(chess_game_id)

        return chess_game

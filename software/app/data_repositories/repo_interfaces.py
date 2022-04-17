from abc import ABC, abstractmethod
from app.models import ChessGame


class IChessGameRepo(ABC):

    @abstractmethod
    def add(self, chess_game: ChessGame):
        pass
from abc import ABC, abstractmethod
from app.models import ChessGame, GamePlayer


class IChessGameRepo(ABC):

    @abstractmethod
    def add(self, chess_game: ChessGame):
        pass


class IGamePlayerRepo(ABC):

    @abstractmethod
    def add(self, game_player: GamePlayer):
        pass

    @abstractmethod
    def get(self, criterion):
        pass

    @abstractmethod
    def exists(self, criterion):
        pass

    @abstractmethod
    def count(self, criterion):
        pass

from abc import ABC, abstractmethod
from app.store import ChessGame, ChessPlayer


class IChessGameRepo(ABC):

    @abstractmethod
    def add_game(self, chess_game: ChessGame):
        pass

    @abstractmethod
    def get_game_by_id(self, chess_game_id: int):
        pass

    @abstractmethod
    def get_games(self, criterion):
        pass

    @staticmethod
    def delete_game(self, criterion):
        pass

    @abstractmethod
    def count(self, criterion):
        pass


class IGamePlayerRepo(ABC):

    @abstractmethod
    def add_player(self, game_player: ChessPlayer):
        pass

    @abstractmethod
    def get_players(self, criterion):
        pass

    @abstractmethod
    def get_player_by_id(self, game_player_id: int):
        pass

    @abstractmethod
    def exists(self, criterion):
        pass

    @abstractmethod
    def count(self, criterion):
        pass

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSlot, pyqtSignal
import typing

from app.data_repositories import IGamePlayerRepo
from app.data_repositories import IChessGameRepo

from app.store import ChessGame

from app.store import AssociationChessPlayerChessGame


class ChessPlayerTableModel(QAbstractTableModel):

    def __init__(self, chess_player_repo: IGamePlayerRepo, criterion):
        super().__init__()
        self._chess_player_repo = chess_player_repo
        self.criterion = criterion

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._chess_player_repo.count(self.criterion)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        game_players = self._chess_player_repo.get_players(self.criterion)

        if not index.isValid():
            return QVariant()

        if index.row() >= len(game_players) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return game_players[index.row()].id
            if index.column() == 1:
                return game_players[index.row()].first_name
            if index.column() == 2:
                return game_players[index.row()].last_name
            if index.column() == 3:
                return game_players[index.row()].date_of_birth
            if index.column() == 4:
                return game_players[index.row()].comment

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return 'ID'
            elif section == 1:
                return 'Имя'
            elif section == 2:
                return 'Фамилия'
            elif section == 3:
                return 'Дата рождения'
            elif section == 4:
                return 'Комментарий'

            return QVariant()


class ChessGameTableModel(QAbstractTableModel):
    data_changed = pyqtSignal(QModelIndex, QModelIndex)

    def __init__(self):
        super().__init__()
        self._chess_games = []

    @property
    def chess_games(self):
        return self._chess_games

    @chess_games.setter
    def chess_games(self, games):
        self._chess_games = games

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 7

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._chess_games)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or self._chess_games is None:
            return QVariant()

        if index.row() >= len(self._chess_games) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._chess_games[index.row()].id
            if index.column() == 1:
                return self._chess_games[index.row()].begin_date
            if index.column() == 2:
                if self._chess_games[index.row()].winner == ChessGame.GameOutcome.white:
                    return '1-0'
                if self._chess_games[index.row()].winner == ChessGame.GameOutcome.black:
                    return '0-1'
                return '1/2-1/2'
            if index.column() == 3:
                white_player = list(filter(lambda e: e.color == AssociationChessPlayerChessGame.Color.white, self._chess_games[index.row()].chess_players))[0].chess_player
                return white_player.first_name + ' ' + white_player.last_name
            if index.column() == 4:
                white_player = list(filter(lambda e: e.color == AssociationChessPlayerChessGame.Color.white, self._chess_games[index.row()].chess_players))[0].chess_player
                return white_player.id
            if index.column() == 5:
                black_player = list(filter(lambda e: e.color == AssociationChessPlayerChessGame.Color.black, self._chess_games[index.row()].chess_players))[0].chess_player
                return black_player.first_name + ' ' + black_player.last_name
            if index.column() == 6:
                black_player = list(filter(lambda e: e.color == AssociationChessPlayerChessGame.Color.black, self._chess_games[index.row()].chess_players))[0].chess_player
                return black_player.id

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return 'ID партии'
            elif section == 1:
                return 'Дата начала'
            elif section == 2:
                return 'Исход'
            elif section == 3:
                return 'Белые'
            elif section == 4:
                return 'ID игрока за белых'
            elif section == 5:
                return 'Чёрные'
            elif section == 6:
                return 'ID игрока за чёрных'

        return QVariant()
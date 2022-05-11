from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
import typing

from app.data_repositories import IGamePlayerRepo


class GamePlayerTableModel(QAbstractTableModel):

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
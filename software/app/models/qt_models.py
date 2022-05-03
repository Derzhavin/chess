from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
import typing

from app.data_repositories import IGamePlayerRepo


class GamePlayerTableModel(QAbstractTableModel):

    def __init__(self, game_player_repo: IGamePlayerRepo, criterion):
        super().__init__()
        self._game_player_repo = game_player_repo
        self.criterion = criterion

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self._game_player_repo.count(self.criterion)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        game_players = self._game_player_repo.get(self.criterion)

        if not index.isValid():
            return QVariant()

        if index.row() >= len(game_players) or index.row() < 0:
            return QVariant()

        if role == Qt.DisplayRole:
            return game_players[index.row()][index.column()]

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
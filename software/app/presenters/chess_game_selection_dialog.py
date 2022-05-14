
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QItemSelection, QAbstractTableModel, QItemSelectionModel
from PyQt5.QtWidgets import QAbstractItemView
from app.models import ChessGameTableModel
from app.data_repositories import IChessGameRepo


class ChessGameSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent, config, chess_game_repo: IChessGameRepo, criterion):
        super().__init__(parent)
        uic.loadUi(config.game_selection_dialog, self)

        self.table_model = ChessGameTableModel(chess_game_repo, criterion)

        self.table_view.setModel(self.table_model)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        selection_model = self.table_view.selectionModel()
        selection_model.selectionChanged.connect(self.on_row_clicked)
        index = self.table_model.index(0, 0)
        selection_model.select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        self.selected_game_id = int(self.table_model.index(0, 0).data())

    def on_row_clicked(self, cur: QItemSelection, prev: QItemSelection):
        self.selected_game_id = int(cur.indexes()[0].data())
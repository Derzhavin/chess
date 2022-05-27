
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QItemSelection, QItemSelectionModel
from PyQt5.QtWidgets import QAbstractItemView
from app.models import ChessGameTableModel
from sqlalchemy.orm import sessionmaker


class ChessGameSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent, config, engine, chess_game_repo_cls):
        super().__init__(parent)
        uic.loadUi(config.game_selection_dialog_ui_path, self)
        self.config = config
        self.session = sessionmaker(engine)()
        self.chess_game_repo = chess_game_repo_cls(self.session)
        self.table_model = ChessGameTableModel()
        self.table_view.setModel(self.table_model)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        selection_model = self.table_view.selectionModel()
        selection_model.selectionChanged.connect(self.on_row_clicked)
        self.selected_game_id = -1
        self.criterion = True

    def load_data(self):
        self.table_model._chess_games = self.chess_game_repo.get_games(self.criterion)

        index = self.table_model.index(0, 0)
        selection_model = self.table_view.selectionModel()
        selection_model.select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        self.selected_game_id = int(index.data())

    def on_row_clicked(self, cur: QItemSelection, prev: QItemSelection):
        self.selected_game_id = int(cur.indexes()[0].data())

    def __del__(self):
        self.session.close()
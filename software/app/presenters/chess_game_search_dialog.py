from datetime import date

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QItemSelection, QItemSelectionModel
from PyQt5.QtWidgets import QAbstractItemView
from app.models import ChessGameTableModel
from sqlalchemy.orm import sessionmaker


class ChessGameSearchDialog(QtWidgets.QDialog):
    def __init__(self, parent, config, engine, chess_game_repo_cls):
        super().__init__(parent)
        uic.loadUi(config.game_search_dialog_ui_path, self)

        self.session = sessionmaker(engine)()
        self.chess_game_repo = chess_game_repo_cls(self.session)
        self.config = config

        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.push_button_find_game.clicked.connect(self.on_push_button_find_game_clicked)
        self.push_button_load_chess_game.clicked.connect(self.accept)
        self.load_data()

        self.selected_game_id = -1

    def load_data(self, target_date: date = None, white_player_first_name_pattern=None,
                  white_player_last_name_pattern=None,
                  black_player_first_name_pattern=None, black_player_last_name_pattern=None):
        self.push_button_load_chess_game.setEnabled(False)

        table_model = ChessGameTableModel()

        table_model.chess_games = self.chess_game_repo \
            .get_games_super_query(target_date, white_player_first_name_pattern, white_player_last_name_pattern,
                                   black_player_first_name_pattern, black_player_last_name_pattern)

        self.table_view.setModel(table_model)
        self.table_view.selectionModel().selectionChanged.connect(self.on_row_clicked)

        if table_model.chess_games:
            index = table_model.index(0, 0)
            self.table_view.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            self.push_button_load_chess_game.setEnabled(True)

    def on_row_clicked(self, cur: QItemSelection, prev: QItemSelection):
        if self.table_view.model().chess_games:
            self.selected_game_id = int(cur.indexes()[0].data())

    def __del__(self):
        self.session.close()

    def on_push_button_find_game_clicked(self):
        if not self.table_view.model().chess_games:
            return
        
        if self.check_box_chess_game_date.isChecked():
            target_date = self.date_edit_chess_game.date().toPyDate()
        else:
            target_date = None

        if self.check_box_white_player_first_name.isChecked():
            white_player_first_name_pattern = self.line_edit_white_player_first_name.text()
        else:
            white_player_first_name_pattern = None

        if self.check_box_white_player_last_name.isChecked():
            white_player_last_name_pattern = self.line_edit_white_player_last_name.text()
        else:
            white_player_last_name_pattern = None

        if self.check_box_black_player_first_name.isChecked():
            black_player_first_name_pattern = self.line_edit_black_player_first_name.text()
        else:
            black_player_first_name_pattern = None

        if self.check_box_white_player_last_name.isChecked():
            black_player_last_name_pattern = self.line_edit_black_player_last_name.text()
        else:
            black_player_last_name_pattern = None

        self.load_data(target_date, white_player_first_name_pattern, white_player_last_name_pattern,
                       black_player_first_name_pattern, black_player_last_name_pattern)
from datetime import date

from PyQt5 import QtWidgets, uic
from enum import Enum

from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QAbstractItemView
from app.models.qt_models import GamePlayerTableModel


class SelectOptPage(QtWidgets.QWidget):
    def __init__(self, parent, config):
        super().__init__(parent)
        uic.loadUi(config.game_player_resolve_step_select_opt_widget, self)


class ChoosePlayerPage(QtWidgets.QWidget):
    def __init__(self, parent, config):
        super().__init__(parent)
        uic.loadUi(config.game_player_resolve_step_choose_player_opt_widget, self)


class CreatePlayerPage(QtWidgets.QWidget):
    def __init__(self, parent, config):
        super().__init__(parent)
        uic.loadUi(config.game_player_resolve_step_create_player_opt_widget, self)


class GamePlayerResolveDialog(QtWidgets.QDialog):

    class SelectedOptionStep(Enum):
        cancel_op, choose_player_op, create_player_op = range(3)

    def __init__(self, parent, config, game_player_repo, criterion):
        super().__init__(parent)
        self.config = config
        self.game_player_repo = game_player_repo
        self.criterion = criterion
        uic.loadUi(config.game_player_resolve_dialog, self)
        self.stacked_widget.removeWidget(self.page_0)
        self.stacked_widget.removeWidget(self.page_1)

        self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op

        self.select_opt_page = SelectOptPage(self, config)
        self.stacked_widget.addWidget(self.select_opt_page)

        self.choose_player_page = ChoosePlayerPage(self, config)
        self.stacked_widget.addWidget(self.choose_player_page)

        self.create_player_page = CreatePlayerPage(self, config)
        self.stacked_widget.addWidget(self.create_player_page)

        self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op
        self.select_opt_page.push_button_next.clicked.connect(self.on_select_opt_page_push_button_next_clicked)
        self.select_opt_page.radio_button_cancel_operation.toggled.connect(self.on_select_opt_page_radio_button_toggled)
        self.select_opt_page.radio_button_choose_player.toggled.connect(self.on_select_opt_page_radio_button_toggled)
        self.select_opt_page.radio_button_create_player.toggled.connect(self.on_select_opt_page_radio_button_toggled)

        self.choose_player_page.push_button_accept.clicked.connect(self.on_choose_player_page_push_button_accept_clicked)
        self.choose_player_page.push_button_back.clicked.connect(self.on_choose_player_page_push_button_back_clicked)

        self.create_player_page.push_button_accept.clicked.connect(self.on_create_player_page_push_button_accept_clicked)
        self.create_player_page.push_button_back.clicked.connect(self.on_create_player_page_push_button_back_clicked)

        self.create_player_page.text_edit_first_name.textChanged.connect(self.on_create_player_page_text_edit_first_name_changed)
        self.create_player_page.text_edit_last_name.textChanged.connect(self.on_create_player_page_text_edit_last_name_changed)
        self.create_player_page.text_edit_date_of_birth.textChanged.connect(self.on_create_player_page_text_edit_date_of_birth_changed)
        self.create_player_page.plaintext_edit_comment.textChanged.connect(self.on_create_player_page_plaintext_edit_comment_changed)

        self.go_to_select_opt_page()

        self.target_chess_player_first_name = ''
        self.target_chess_player_last_name = ''
        self.target_chess_player_date_of_birth = date.today()
        self.target_chess_player_comment = ''

    def go_to_select_opt_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_choose_player_page(self):
        self.stacked_widget.setCurrentIndex(1)

        game_player_table_model = GamePlayerTableModel(self.game_player_repo, self.criterion)

        self.choose_player_page.table_view_game_players.setModel(game_player_table_model)
        self.choose_player_page.table_view_game_players.setSelectionMode(QAbstractItemView.SingleSelection)
        self.choose_player_page.table_view_game_players.setSelectionBehavior(QAbstractItemView.SelectRows)

        index = game_player_table_model.index(0, 0)
        selection_model = self.choose_player_page.table_view_game_players.selectionModel()
        selection_model.select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)

    def go_to_create_player_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def on_select_opt_page_push_button_next_clicked(self):
        if self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.cancel_op:
            self.close()
            return
        if self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
            self.go_to_choose_player_page()
        elif self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.create_player_op:
            self.go_to_create_player_page()

    def on_select_opt_page_radio_button_toggled(self):
        if self.select_opt_page.radio_button_cancel_operation.isChecked():
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op
        elif self.select_opt_page.radio_button_choose_player.isChecked():
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.choose_player_op
        else:
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.create_player_op

    def on_create_player_page_push_button_accept_clicked(self):
        self.accept()

    def on_create_player_page_push_button_back_clicked(self):
        self.go_to_select_opt_page()

    def on_choose_player_page_push_button_accept_clicked(self):
        self.accept()

    def on_choose_player_page_push_button_back_clicked(self):
        self.go_to_select_opt_page()

    def on_create_player_page_text_edit_first_name_changed(self, first_name: str):
        self.target_chess_player_first_name = first_name

    def on_create_player_page_text_edit_last_name_changed(self, last_name: str):
        self.target_chess_player_first_name = last_name

    def on_create_player_page_text_edit_date_of_birth_changed(self, date_of_birth: str):
        self.target_chess_player_first_name = date.fromisoformat(date_of_birth)

    def on_create_player_page_plaintext_edit_comment_changed(self, comment: str):
        self.target_chess_player_comment = comment

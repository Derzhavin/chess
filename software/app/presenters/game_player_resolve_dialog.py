from PyQt5 import QtWidgets, uic
from enum import Enum

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

        # self.create_player_page = CreatePlayerPage(self, config)
        # self.stacked_widget.addWidget(self.create_player_page)

        self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op
        self.select_opt_page.push_button_next.clicked.connect(self.on_push_button_next_clicked)
        self.select_opt_page.radio_button_cancel_operation.toggled.connect(self.on_radio_button_toggled)
        self.select_opt_page.radio_button_choose_player.toggled.connect(self.on_radio_button_toggled)
        self.select_opt_page.radio_button_create_player.toggled.connect(self.on_radio_button_toggled)

        self.go_to_select_page()
        self.show()

    def go_to_select_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def go_to_choose_player_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_create_player_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def on_push_button_next_clicked(self):
        if self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.cancel_op:
            self.close()
            return
        if self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
            self.go_to_choose_player_page()
            self.choose_player_page.table_view_game_players.setModel(GamePlayerTableModel(self.game_player_repo, self.criterion))
        elif self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
            self.go_to_create_player_page()

    def on_radio_button_toggled(self):
        if self.select_opt_page.radio_button_cancel_operation.isChecked():
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op
        elif self.select_opt_page.radio_button_choose_player.isChecked():
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.choose_player_op
        else:
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.create_player_op


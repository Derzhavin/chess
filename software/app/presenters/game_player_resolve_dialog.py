from PyQt5 import QtWidgets, uic
from enum import Enum

from app.models.qt_models import GamePlayerTableModel


class GamePlayerResolveDialog(QtWidgets.QDialog):

    class SelectedOptionStep(Enum):
        cancel_op, choose_player_op, create_player = range(3)

    def __init__(self, parent, config, game_player_repo):
        super().__init__(parent)
        self.config = config

        uic.loadUi(config.game_player_resolve_step_select_opt_dialog, self)

        self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op

    def on_push_button_next_clicked(self):
        if self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.cancel_op:
            self.close()

        elif self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
            uic.loadUi(self.config.game_player_resolve_step_choose_player_opt_dialog, self)

            self.table_view_game_players.setModel(GamePlayerTableModel())
        elif self.selected_option == GamePlayerResolveDialog.SelectedOptionStep.choose_player_op:
            uic.loadUi(self.config.game_player_resolve_step_create_player_opt_dialog, self)

    def on_radio_button_toggled(self):
        if self.radio_button_cancel_operation.isChecked():
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.cancel_op

        elif self.radio_button_choose_player.isChecked():
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.choose_player_op

        else:
            self.selected_option = GamePlayerResolveDialog.SelectedOptionStep.create_player


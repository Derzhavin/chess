from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QItemSelection, QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableView

from app.views.chessboard import ChessBoardView
from app.controllers.game_controllers import GameController
from app.data_repositories import ChessGameRepo, ChessPlayerRepo
from app.services import PgnImportService, ChessGameDeleteService, ChessGameLoadService

from app.presenters import ChessGameSearchDialog
from app.models import GameMovesTableModel
from app.assets_factory import AssetsFactory
from sqlalchemy.orm import Session


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, engine, config):
        super().__init__()
        uic.loadUi(config.main_window_ui_path, self)
        self.config = config
        self.board_graphics_view.setBackgroundBrush(QColor(config.chessboard_view_background_color))
        self.board_graphics_view.zoom_in_factor = config.chessboard_zoom_in_factor
        self._chessboard_view = ChessBoardView(self.board_graphics_view, config)

        self._game_controller = GameController(self._chessboard_view)
        self._game_controller.game_finished_sig.connect(self.on_game_finished)
        self._game_controller.game_returned_to_begin_sig.connect(self.on_game_returned_to_begin)
        self._game_controller.game_started_sig.connect(self.on_game_started)
        self._game_controller.game_move_changed.connect(self.on_game_move_changed)
        self._game_controller.represent_position()

        self.engine = engine
        self.import_game_action.triggered.connect(self.on_game_import_triggered)
        self.action_delete_game.triggered.connect(self.on_game_delete_triggered)
        self.action_find_chess_game.triggered.connect(self.on_find_chess_game_triggered)

        self.play_tool_button.clicked.connect(self.on_play_button_clicked)
        self.prev_step_tool_button.clicked.connect(self.on_prev_step_button_clicked)
        self.next_step_tool_button.clicked.connect(self.on_next_step_button_clicked)

        self.table_view_moves.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.update_pos = True

    def on_game_import_triggered(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Game (*.pgn)")
        file_dialog.setWindowTitle("Импорт игры")

        if file_dialog.exec():
            pgn_path = file_dialog.selectedFiles()[0]
            pgn_import_service = PgnImportService(self.engine, ChessGameRepo, ChessPlayerRepo)
            pgn_import_service.load_game_from_pgn(pgn_path, self, self.config)

    def on_game_delete_triggered(self):
        chess_game_delete_service = ChessGameDeleteService(self.config, self, self.engine, ChessGameRepo)
        chess_game_delete_service.delete_game()

    def on_find_chess_game_triggered(self):
        with Session(self.engine) as session:
            chess_game_repo = ChessGameRepo(session)
            if chess_game_repo.count(True) < 1:
                QMessageBox.information(self, 'Поиск партии', 'В базе данных отсутствуют партии.')
                return

        chess_game_search_dialog = ChessGameSearchDialog(self, self.config, self.engine, ChessGameRepo)
        chess_game_search_dialog.load_data()

        if chess_game_search_dialog.exec() and chess_game_search_dialog.selected_game_id > -1:
            chess_game_load_service = ChessGameLoadService(self.engine, ChessGameRepo)
            chess_game = chess_game_load_service.load_game(chess_game_search_dialog.selected_game_id)

            game_moves_table_model = GameMovesTableModel()
            game_moves_table_model.moves = chess_game.moves
            self.table_view_moves.setModel(game_moves_table_model)
            selection_model = self.table_view_moves.selectionModel()
            selection_model.selectionChanged.connect(self.on_row_moves_clicked)
            self._game_controller.game = chess_game
            self._show_paused_mode()

    @pyqtSlot()
    def on_play_button_clicked(self):
        if self._game_controller.game.positions_num < 1:
            return
        self.table_view_moves.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self._game_controller.game_on = not self._game_controller.game_on

    @pyqtSlot()
    def on_prev_step_button_clicked(self):
        self._game_controller.do_prev_move()

    @pyqtSlot()
    def on_next_step_button_clicked(self):
        self._game_controller.do_next_move()

    def on_game_finished(self):
        self.table_view_moves.clearSelection()
        self.table_view_moves.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self._game_controller.to_begin()

    def on_game_started(self):
        self._show_playing_mode()

    def on_game_returned_to_begin(self):
        self._show_paused_mode()

    def _show_paused_mode(self):
        self.play_tool_button.setIcon(AssetsFactory().play_tool_button_pixmap)
        self.prev_step_tool_button.setEnabled(False)
        self.next_step_tool_button.setEnabled(False)

    def _show_playing_mode(self):
        self.play_tool_button.setIcon(AssetsFactory().pause_tool_button_pixmap)
        self.prev_step_tool_button.setEnabled(True)
        self.next_step_tool_button.setEnabled(True)

    def on_game_move_changed(self):
        pos = self._game_controller.game.cur_pos
        next_index = self.table_view_moves.model().index((pos - 1) // 2, 1 if pos % 2 else 2)
        self.update_pos = False
        self.table_view_moves.setCurrentIndex(next_index)

    def on_row_moves_clicked(self, cur: QItemSelection, prev: QItemSelection):
        if not cur.indexes() or not self.update_pos:
            self.update_pos = True
            return
        index = cur.indexes()[0]

        pos_no = index.row() * 2 + (index.column())

        if index.column() != 0 and pos_no < self._game_controller.game.positions_num:
            self._game_controller.move_to_pos_index(pos_no)

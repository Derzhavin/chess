from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.orm import sessionmaker
from app.presenters import ChessGameSelectionDialog, WaitDialog
from app.data_repositories import ChessGameRepo
from app.store import ChessGame
from app.multithreading import Worker


class ChessGameDeleter:

    def __init__(self, engine, criterion, chess_game_repo_cls):
        self.engine = engine
        self.chess_game_repo_cls = chess_game_repo_cls
        self.criterion = criterion

    def delete_game(self):
        self.session = sessionmaker(self.engine)()
        self.session.begin()
        chess_game_repo = self.chess_game_repo_cls(self.session)
        chess_game_repo.delete_game(self.criterion)
        self.session.commit()
        self.session.close()


class ChessGameDeleteWorker(Worker):

    def __init__(self, chess_game_deleter: ChessGameDeleter):
        super().__init__()
        self.chess_game_deleter = chess_game_deleter

    @pyqtSlot()
    def run(self):
        self.chess_game_deleter.delete_game()
        self.finished.emit()


class ChessGameDeleteService:

    def __init__(self, config, parent_widget, engine, chess_game_repo_cls):
        self.session = sessionmaker(engine)()
        self.engine = engine
        self.chess_game_repo = chess_game_repo_cls(self.session)
        self.config = config
        self.parent_widget = parent_widget

    def delete_game(self):
        chess_game_repo = ChessGameRepo(self.session)

        if chess_game_repo.count(True) > 0:
            chess_game_selection_dialog = ChessGameSelectionDialog(self.parent_widget, self.config, chess_game_repo, True)

            if chess_game_selection_dialog.exec():
                game_id = chess_game_selection_dialog.selected_game_id
                thread = QThread()

                wait_dialog = WaitDialog(self.parent_widget, self.config)

                chess_game_deleter = ChessGameDeleter(self.engine, (ChessGame.id == game_id), ChessGameRepo)
                chess_game_delete_worker = ChessGameDeleteWorker(chess_game_deleter)
                chess_game_delete_worker.move_to_thread(thread)

                def on_chess_game_delete_worker_finished():
                    wait_dialog.info = 'Партия была успешно удалена.'

                chess_game_delete_worker.finished.connect(on_chess_game_delete_worker_finished)
                chess_game_delete_worker.finished.connect(wait_dialog.on_completed)

                thread.start()

                if wait_dialog.exec() == QtWidgets.QDialog.Rejected:
                    if not thread.isFinished():
                        thread.quit()

        else:
            QMessageBox.information(self.parent_widget, 'Информация', 'В базе данных отсутствуют партии.')


    def __del__(self):
        self.session.close()
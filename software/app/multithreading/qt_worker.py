from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from sqlalchemy.orm import sessionmaker, Session


class Worker(QObject):
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        raise Exception('Worker is abstract class. You must implement run() with @pyqtSlot() deco')
        pass

    def move_to_thread(self, thread: QThread):
        thread.started.connect(self.run)
        self.finished.connect(thread.quit)
        self.finished.connect(self.deleteLater)
        thread.finished.connect(thread.deleteLater)
        self.moveToThread(thread)


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
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


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
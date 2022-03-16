import sys

from PyQt5.QtWidgets import QApplication

from app import App
from config import Config


def main():
    q_app = QApplication(sys.argv)

    app = App(Config)
    app.start()

    q_app.exec_()


if __name__ == '__main__':
    main()
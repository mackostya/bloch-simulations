import sys

from PyQt5.QtWidgets import QApplication
from src.qt.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 500)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

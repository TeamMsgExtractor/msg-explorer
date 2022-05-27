from .main_window import MainWindow

from PySide6.QtWidgets import QApplication


def mainRunner():
    app = QApplication([])
    widget = MainWindow()
    widget.show()

    return app.exec()

# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        # Register the ui with this widget.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

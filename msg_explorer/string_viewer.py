# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_string_viewer import Ui_StringViewer


class StringViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_StringViewer()
        self.ui.setupUi(self)

    @Slot()
    def clear(self):
        self.ui.labelType.setText('')
        self.textDisplay.setPlainText('')

    @Slot(str, str)
    def loadString(self, data, _type):
        """
        Displays the specified string as well as the exact
        type the data was.
        """
        self.ui.labelType.setText('UTF-16-LE String' if _type == '001F' else 'Non-Unicode String')
        self.ui.textDisplay.setPlainText(data)

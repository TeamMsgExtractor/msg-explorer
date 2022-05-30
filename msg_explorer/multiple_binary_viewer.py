# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_multiple_binary_viewer import Ui_MultipleBinaryViewer


class MultipleBinaryViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MultipleBinaryViewer()
        self.ui.setupUi(self)
        self.__entries = []

        self.ui.comboBoxEntries.currentIndexChanged.connect(self._comboBoxChanged)

    @Slot(int)
    def _comboBoxChanged(self, index):
        """
        Change what is being displayed with the combo box changes.
        """
        if index >= 0:
            self.ui.hexViewer.loadHexData(self.__entries[index])
        else:
            self.ui.hexViewer.loadHexData(b'')

    @Slot()
    def clear(self):
        """
        Clear the displayed data.
        """
        self.__entries.clear()
        self.ui.hexViewer.clear()
        self.ui.comboBoxEntries.clear()

    @Slot(list)
    def loadMultiple(self, entries):
        """
        Load the sequence of binary entries into the widget for viewing.
        """
        self.__entries.clear()
        self.__entries.extend(entries)
        self.ui.comboBoxEntries.addItems(tuple(str(x) for x in range(1, len(self.__entries) + 1)))
        self.ui.comboBoxEntries.setCurrentIndex(0 if len(self.__entries) > 0 else -1)

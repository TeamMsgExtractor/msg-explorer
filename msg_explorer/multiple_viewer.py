# This Python file uses the following encoding: utf-8
import datetime

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from . import utils
from .ui.ui_multiple_viewer import Ui_MultipleViewer


_DATE_TYPE_STRINGS = {
    '1002': 'Multiple 16-Bit Integers',
    '1003': 'Multiple 32-Bit Integers',
    '1004': 'Multiple Floats',
    '1005': 'Multiple Double',
    '1006': 'Multiple Currencies',
    '1007': 'Multiple Floating Times',
    '1014': 'Multiple 64-Bit Integers',
    '101E': 'Multiple Non-Unicode Strings',
    '101F': 'Multiple UTF-16-LE Strings',
    '1040': 'Multiple Times',
    '1048': 'Multiple GUIDs',
}


class MultipleViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MultipleViewer()
        self.ui.setupUi(self)

    @Slot()
    def clear(self):
        """
        Clear the displayed data.
        """
        self.ui.labelType.setText('')
        self.ui.listEntries.clear()

    @Slot(list, str)
    def loadMultiple(self, entries, _type):
        self.ui.labelType.setText(_DATE_TYPE_STRINGS[_type])
        self.ui.listEntries.addItems(self.__dataToStrings(entries))

    def __dataToStrings(self, entries):
        """
        Converts the list of data into a tuple of strings.
        """
        # TODO This is a temporary code until it can be finalized.
        return tuple(utils.dataToString(x) for x in entries)

# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_guid_viewer import Ui_GuidViewer


class GuidViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_GuidViewer()
        self.ui.setupUi(self)

    @Slot()
    def clear(self):
        self.ui.labelGuid.setText('')

    @Slot(object)
    def loadGuid(self, guid):
        self.ui.labelGuid.setText(guid)

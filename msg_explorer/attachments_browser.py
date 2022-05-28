# This Python file uses the following encoding: utf-8
import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_attachments_browser import Ui_AttachmentsBrowser


class AttachmentsBrowser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_AttachmentsBrowser()
        self.ui.setupUi(self)

    @Slot()
    def msgClosed(self):
        pass

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        pass

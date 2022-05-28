# This Python file uses the following encoding: utf-8
import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_msg_details_page import Ui_MSGDetailsPage


class MSGDetailsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MSGDetailsPage()
        self.ui.setupUi(self)

    @Slot()
    def msgClosed(self):
        self.ui.labelPath.setText('No File Loaded')
        self.ui.labelClass.setText('')
        self.ui.labelClassType.setText('')
        self.ui.labelEncoding.setText('')
        self.ui.labelAttachCount.setText('')
        self.ui.labelRecipCount.setText('')

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        self.ui.labelPath.setText(msgFile.path)
        self.ui.labelClass.setText(msgFile.__class__.__name__)
        self.ui.labelClassType.setText(msgFile.classType)
        self.ui.labelEncoding.setText(msgFile.stringEncoding)
        self.ui.labelAttachCount.setText(str(len(msgFile.attachments)))
        self.ui.labelRecipCount.setText(str(len(msgFile.recipients)))

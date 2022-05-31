# This Python file uses the following encoding: utf-8
import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT
from PySide6.QtWidgets import QTableWidgetItem

from .ui.ui_attachments_browser import Ui_AttachmentsBrowser


class AttachmentsBrowser(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_AttachmentsBrowser()
        self.ui.setupUi(self)

    @Slot()
    def msgClosed(self):
        self.ui.tableAttachments.clearContents()

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        try:
            self.ui.tableAttachments.setRowCount(len(msgFile.attachments))
            for index, att in enumerate(msgFile.attachments):
                self.ui.tableAttachments.setItem(index, 0, QTableWidgetItem(str(index)))
                if isinstance(att, extract_msg.Attachment):
                    self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("OK"))
                    self.ui.tableAttachments.setItem(index, 2, QTableWidgetItem(att.shortFilename))
                    self.ui.tableAttachments.setItem(index, 3, QTableWidgetItem(att.longFilename))
                    self.ui.tableAttachments.setItem(index, 4, QTableWidgetItem(att.cid))
                    self.ui.tableAttachments.setItem(index, 5, QTableWidgetItem(str(att.renderingPosition)))
                elif isinstance(att, extract_msg.attachment.BrokenAttachment):
                    self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("Broken"))
                elif isinstance(att, extract_msg.attachment.UnsupportedAttachment):
                    self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("Unsupported"))
                else:
                    self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("Unknown Type"))
        except AttributeError as e:
            print(e)

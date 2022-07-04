# This Python file uses the following encoding: utf-8
import logging

import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT
from PySide6.QtWidgets import QTableWidgetItem

from .ui.ui_attachments_browser import Ui_AttachmentsBrowser


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AttachmentsBrowser(QtWidgets.QWidget):
    # Signals that an attachment was double clicked.
    attachmentSelected = Signal(int)
    signedAttachmentSelected = Signal(int)
    def __init__(self, parent = None):
        super().__init__(parent)

        self.ui = Ui_AttachmentsBrowser()
        self.ui.setupUi(self)

        self.ui.tableAttachments.cellDoubleClicked.connect(self._cellDoubleClicked)
        self.__isSigned = False

    @Slot()
    def msgClosed(self):
        self.ui.tableAttachments.clearContents()
        self.ui.tableAttachments.setRowCount(0)

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        self.__isSigned = isinstance(msgFile, extract_msg.MessageSignedBase)
        totalAttachments = len(msgFile.attachments)
        if self.__isSigned:
            totalAttachments += len(msgFile._rawAttachments)
        self.ui.tableAttachments.setRowCount(totalAttachments)
        indexPostfix = ' (Regular)' if self.__isSigned else ''
        count = 0
        self.ui.tableAttachments.setSortingEnabled(False)
        for index, att in enumerate(msgFile._rawAttachments if self.__isSigned else msgFile.attachments):
            self.ui.tableAttachments.setItem(index, 0, QTableWidgetItem(str(index) + indexPostfix))
            if isinstance(att, extract_msg.Attachment):
                self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("OK"))
            elif isinstance(att, extract_msg.attachment.BrokenAttachment):
                self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("Broken"))
            elif isinstance(att, extract_msg.attachment.UnsupportedAttachment):
                self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("Unsupported"))
            else:
                self.ui.tableAttachments.setItem(index, 1, QTableWidgetItem("Unknown Type"))
            self.ui.tableAttachments.setItem(index, 2, QTableWidgetItem(att.shortFilename))
            self.ui.tableAttachments.setItem(index, 3, QTableWidgetItem(att.longFilename))
            self.ui.tableAttachments.setItem(index, 4, QTableWidgetItem(att.cid))
            print(att.mimetype)
            self.ui.tableAttachments.setItem(index, 5, QTableWidgetItem(att.mimetype))
            self.ui.tableAttachments.setItem(index, 6, QTableWidgetItem("Not Rendered" if att.renderingPosition and att.renderingPosition == 0xFFFFFFFF else str(att.renderingPosition)))
            count += 1
        if self.__isSigned:
            # If it's signed, also display the regular attachments.
            for index, att in enumerate(msgFile.attachments):
                self.ui.tableAttachments.setItem(count + index, 0, QTableWidgetItem(str(index)))
                self.ui.tableAttachments.setItem(count + index, 1, QTableWidgetItem("OK (Signed)"))
                self.ui.tableAttachments.setItem(count + index, 2, QTableWidgetItem(att.name))
                self.ui.tableAttachments.setItem(count + index, 3, QTableWidgetItem(att.name))
                self.ui.tableAttachments.setItem(count + index, 5, QTableWidgetItem(att.mimetype))

        self.ui.tableAttachments.setSortingEnabled(True)

    @Slot(int, int)
    def _cellDoubleClicked(self, row : int, column : int):
        """
        Handle a cell being double clicked to emit the attachmentSelected signal.
        """
        if row < self.ui.tableAttachments.rowCount():
            data = self.ui.tableAttachments.item(row, 0).data(0)
            if self.__isSigned:
                if data.endswith(')'):
                    # Regular attachment.
                    self.attachmentSelected.emit(data.split(' ')[0])
                else:
                    # Signed attachment.
                    self.signedAttachmentSelected.emit(int(data))
            else:
                self.attachmentSelected.emit(int(data))
        else:
            logger.warn(f'Received index on cell double click that was outside of table (row: {row}, colunn {column}).')

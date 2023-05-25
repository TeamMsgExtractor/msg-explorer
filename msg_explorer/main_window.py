# This Python file uses the following encoding: utf-8
import os
import pathlib
import threading

import extract_msg

from PySide6.QtCore import QEventLoop, Signal, SIGNAL, Slot, SLOT
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QWidget

from . import app_icons, font_handler, hex_viewer, utils, __version__
from .logger_widget import LoggerWidget
from .ui.ui_main_window import Ui_MainWindow
from .ui.ui_loading_screen import Ui_LoadingScreen


class MainWindow(QMainWindow):
    # A signal that announces the msg file has been closed. Makes it easier
    # to communicate to any components that need it so the close function
    # doesn't have to be modified, just the signal/slot connections.
    msgClosed = Signal()
    msgOpened = Signal(extract_msg.msg.MSGFile)
    # A signal which announces a desire to have the event loop process once.
    processEventLoop = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)

        # Register the ui with this widget.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the menu bar slots.
        self.ui.actionLoad_Msg_File.triggered.connect(self.loadMsgFile)
        self.ui.actionLoad_Parent_Msg.triggered.connect(self.loadParent)
        self.ui.actionClose_Current_File.triggered.connect(self.closeFile)
        self.ui.actionOpen_Log.triggered.connect(self._showLogWindow)
        self.ui.actionExport_Current_File.triggered.connect(self.exportFile)

        # Connect the pages to the opening and closing of the msg file.
        self.msgOpened.connect(self.ui.pageBasicInformation.msgOpened)
        self.msgOpened.connect(self.ui.pageTreeView.msgOpened)
        self.msgOpened.connect(self.ui.pageAttachments.msgOpened)
        self.msgOpened.connect(self.ui.pageNamedProperties.msgOpened)
        self.msgOpened.connect(self.ui.pageStreamView.msgOpened)
        self.msgClosed.connect(self.ui.pageBasicInformation.msgClosed)
        self.msgClosed.connect(self.ui.pageTreeView.msgClosed)
        self.msgClosed.connect(self.ui.pageAttachments.msgClosed)
        self.msgClosed.connect(self.ui.pageNamedProperties.msgClosed)
        self.msgClosed.connect(self.ui.pageStreamView.msgClosed)

        # Connect the double click from the tree to the stream view.
        self.ui.pageTreeView.fileDoubleClicked.connect(self.ui.pageStreamView.openStream)
        self.ui.pageTreeView.fileDoubleClicked.connect(self._streamSelected)
        self.ui.pageNamedProperties.namedPropertySelected.connect(self.ui.pageStreamView.openStream)
        self.ui.pageNamedProperties.namedPropertySelected.connect(self._streamSelected)

        self.ui.actionIncrease_Font.triggered.connect(self.increaseFont)
        self.ui.actionDecrease_Font.triggered.connect(self.decreaseFont)

        self.ui.pageAttachments.attachmentSelected.connect(self.attachmentSelected)
        self.ui.pageAttachments.signedAttachmentSelected.connect(self.signedAttachmentSelected)

        font_handler.getFontHandler().registerFont(self.font, self.setFont)

        self.__msg = None
        self.__parentMsgs = []

        self.__logger = LoggerWidget()

        self.mainIcon = QIcon(QPixmap(":/icon/envelope_1024.png"))
        self.setWindowIcon(self.mainIcon)

        # Attempt to set the actual icon on the taskbar in windows.
        if os.name == 'nt':
            import ctypes
            appid = f'TeamMsgExtractor.MSGExplorer.{__version__}'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    def closeEvent(self, event):
        """
        Override the default close function to cause all windows to be
        closed by this function before running default close.
        """
        QApplication.closeAllWindows()

    def dragEnterEvent(self, event):
        # Handle a file being drag and dropped onto this window.
        mime = event.mimeData()
        if mime.hasUrls() and len(mime.urls()) == 1 and mime.urls()[0].isLocalFile():
            # We know it has exactly one local url, so let's check it.
            f = pathlib.Path(mime.urls()[0].toLocalFile())
            if f.suffix.lower() == '.msg' and f.is_file():
                event.acceptProposedAction()

    def dropEvent(self, event):
        if QMessageBox.question(self, self.tr('Open Msg?'), self.tr('Are you sure you want to open this MSG file?')) == QMessageBox.Yes:
            event.acceptProposedAction()
            self.loadMsgFile(event.mimeData().urls()[0].toLocalFile())

    @Slot(int)
    def attachmentSelected(self, index):
        if isinstance(self.__msg, extract_msg.MessageSignedBase):
            attachment = self.__msg._rawAttachments[index]
        else:
            attachment = self.__msg.attachments[index]

        if isinstance(attachment, extract_msg.Attachment):
            if attachment.type == extract_msg.enums.AttachmentType.DATA:
                self.ui.pageStreamView.openStream(attachment.dir.split('/') + ['__substg1.0_37010102'])
                self.ui.tabWidget.setCurrentWidget(self.ui.pageStreamView)
            elif attachment.type == extract_msg.enums.AttachmentType.MSG:
                if QMessageBox.question(self, self.tr('Open Embedded Msg'), self.tr('Would you like to open the embedded MSG file?')) == QMessageBox.Yes:
                    self.__parentMsgs.append(self.__msg)
                    self.__msg = attachment.data
                    self.msgClosed.emit()
                    self.msgOpened.emit(self.__msg)
                    self.ui.actionLoad_Parent_Msg.setEnabled(True)

    @Slot()
    def closeFile(self):
        """
        Closes the current MSG file and cleans up all the UI components.
        """
        if self.__msg:
            if self.__parentMsgs:
                self.__parentMsgs[0].close()
                self.__parentMsgs.clear()
            else:
                self.__msg.close()
            self.__msg = None
            self.msgClosed.emit()
            self.ui.actionClose_Current_File.setEnabled(False)
            self.ui.actionLoad_Parent_Msg.setEnabled(False)
            self.ui.actionExport_Current_File.setEnabled(False)

    @Slot()
    def exportFile(self):
        """
        Export the currently opened MSG file to the location the user provides.
        """
        filename = QFileDialog.getSaveFileName(self, self.tr('Export File'), filter = self.tr('MSG files (*.msg)'))
        if filename[0]:
            try:
                self.__msg.export(filename[0])
                QMessageBox.information(self, self.tr('Export Complete'), f'Exported to "{filename[0]}"')
            except Exception as e:
                utils.displayException(e)

    @Slot()
    def loadMsgFile(self, path = None):
        """
        Brings up a dialog to load a specific MSG file.
        """
        if path:
            msgPath = path
        else:
            msgPath = QFileDialog.getOpenFileName(filter = self.tr('MSG files (*.msg)'))[0]
        if msgPath:
            # Create a popup for the loading screen.
            loadingScreenWidget = QWidget()
            loadingScreen = Ui_LoadingScreen()
            loadingScreen.setupUi(loadingScreenWidget)
            loadingScreenWidget.show()

            # We run the loading in a new thread so the ui can still update.
            output = [None]
            thread = threading.Thread(target = self._loadMsgThread, args = (msgPath, output,), daemon = True)
            thread.start()

            # Wait for the thread to finish and keep updating the ui.
            while thread.is_alive():
                self.processEventLoop.emit()

            # Check for an error from the thread.
            if isinstance(output[0], Exception):
                if isinstance(output[0], extract_msg.exceptions.InvalidFileFormatError):
                    QMessageBox.critical(self, self.tr('Error'), self.tr('File is not an MSG file.'))
                else:
                    utils.displayException(output[0])
            else:
                self.closeFile()
                self.__msg = output[0]
                loadingScreen.loadingMessage.setText(self.tr('Finishing up...'))
                self.processEventLoop.emit()
                self.msgOpened.emit(self.__msg)

            del loadingScreenWidget

            self.ui.actionClose_Current_File.setEnabled(True)
            self.ui.actionExport_Current_File.setEnabled(True)

    @Slot()
    def loadParent(self):
        """
        Moves to the parent msg file.
        """
        if self.__parentMsgs:
            self.__msg = self.__parentMsgs.pop()
            self.msgClosed.emit()
            self.msgOpened.emit(self.__msg)
            if not self.__parentMsgs:
                self.ui.actionLoad_Parent_Msg.setEnabled(False)
        else:
            QMessageBox.critical(self, self.tr('Error'), self.tr('No parent MSG file.'))

    def _loadMsgThread(self, msgPath, output):
        try:
            msgFile = extract_msg.openMsg(msgPath, errorBehavior = extract_msg.enums.ErrorBehavior.SUPPRESS_ALL, strict = False)
            output[0] = msgFile
        except Exception as e:
            output[0] = e

    @Slot(int)
    def signedAttachmentSelected(self, index : int):
        """
        Handle a signed attachment being selected.
        """
        att = self.__msg.attachments[index]
        self.ui.pageStreamView.openStreamBytes(f'Signed Attachment: {att.name}', att.data)
        self.ui.tabWidget.setCurrentWidget(self.ui.pageStreamView)

    @Slot()
    def _showLogWindow(self):
        self.__logger.show()

    @Slot(object)
    def _streamSelected(self, *args):
        self.ui.tabWidget.setCurrentWidget(self.ui.pageStreamView)

    @Slot()
    def increaseFont(self):
        font_handler.getFontHandler().increaseFonts()

    @Slot()
    def decreaseFont(self):
        font_handler.getFontHandler().decreaseFonts()

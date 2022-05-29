# This Python file uses the following encoding: utf-8
import threading

import extract_msg

from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QWidget
from PySide6.QtCore import QEventLoop, Signal, SIGNAL, Slot, SLOT

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
        self.ui.actionClose_Current_File.triggered.connect(self.closeFile)

        # Connect the pages to the opening and closing of the msg file.
        self.msgOpened.connect(self.ui.pageBasicInformation.msgOpened)
        self.msgOpened.connect(self.ui.pageAttachments.msgOpened)
        self.msgOpened.connect(self.ui.pageRawView.msgOpened)
        self.msgOpened.connect(self.ui.pageStreamView.msgOpened)
        self.msgClosed.connect(self.ui.pageBasicInformation.msgClosed)
        self.msgClosed.connect(self.ui.pageAttachments.msgClosed)
        self.msgClosed.connect(self.ui.pageRawView.msgClosed)
        self.msgClosed.connect(self.ui.pageStreamView.msgClosed)

        self.__msg = None

    @Slot()
    def closeFile(self):
        """
        Closes the current MSG file and cleans up all the UI components.
        """
        if self.__msg:
            self.__msg.close()
            self.__msg = None
            self.msgClosed.emit()

    @Slot()
    def loadMsgFile(self):
        """
        Brings up a dialog to load a specific MSG file.
        """
        msgPath = QFileDialog.getOpenFileName(filter = self.tr('MSG Files (*.msg)'))
        if msgPath[0]:
            # Create a popup for the loading screen.
            loadingScreenWidget = QWidget()
            loadingScreen = Ui_LoadingScreen()
            loadingScreen.setupUi(loadingScreenWidget)
            loadingScreenWidget.show()

            output = [None]
            thread = threading.Thread(target = self._loadMsgThread, args = (msgPath, output,), daemon = True)
            thread.start()

            while thread.is_alive():
                self.processEventLoop.emit()

            if isinstance(output[0], Exception):
                QMessageBox.critical(None, 'Error', 'File is not an MSG file.')
            else:
                self.closeFile()
                self.__msg = output[0]
                self.msgOpened.emit(self.__msg)

            del loadingScreenWidget

    def _loadMsgThread(self, msgPath, output):
        try:
            msgFile = extract_msg.openMsg(msgPath[0], attachmentErrorBehavior = extract_msg.constants.ATTACHMENT_ERROR_BROKEN, strict = False)
            output[0] = msgFile
        except extract_msg.exceptions.InvalidFileFormatError as e:
            output[0] = e


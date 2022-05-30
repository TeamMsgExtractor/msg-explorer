# This Python file uses the following encoding: utf-8
import threading

import extract_msg

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QWidget
from PySide6.QtCore import QEventLoop, Signal, SIGNAL, Slot, SLOT

from . import font_handler, hex_viewer, utils
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
        self.msgOpened.connect(self.ui.pageTreeView.msgOpened)
        self.msgOpened.connect(self.ui.pageStreamView.msgOpened)
        self.msgClosed.connect(self.ui.pageBasicInformation.msgClosed)
        self.msgClosed.connect(self.ui.pageAttachments.msgClosed)
        self.msgClosed.connect(self.ui.pageTreeView.msgClosed)
        self.msgClosed.connect(self.ui.pageStreamView.msgClosed)

        # Connect the double click from the tree to the stream view.
        self.ui.pageTreeView.fileDoubleClicked.connect(self.ui.pageStreamView.openStream)
        self.ui.pageTreeView.fileDoubleClicked.connect(self._streamSelected)

        self.ui.actionIncrease_Font.triggered.connect(self.increaseFont)
        self.ui.actionDecrease_Font.triggered.connect(self.decreaseFont)

        font_handler.getFontHandler().registerFont(self.font, self.setFont)

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
                    QMessageBox.critical(None, 'Error', 'File is not an MSG file.')
                else:
                    utils.displayException(output[0])
            else:
                self.closeFile()
                self.__msg = output[0]
                loadingScreen.loadingMessage.setText('Finishing up...')
                self.processEventLoop.emit()
                self.msgOpened.emit(self.__msg)

            del loadingScreenWidget

    def _loadMsgThread(self, msgPath, output):
        try:
            msgFile = extract_msg.openMsg(msgPath[0], attachmentErrorBehavior = extract_msg.constants.ATTACHMENT_ERROR_BROKEN, strict = False)
            output[0] = msgFile
        except Exception as e:
            output[0] = e

    @Slot(object)
    def _streamSelected(self, *args):
        self.ui.tabWidget.setCurrentWidget(self.ui.pageStreamView)

    @Slot()
    def increaseFont(self):
        font_handler.getFontHandler().increaseFonts()

    @Slot()
    def decreaseFont(self):
        font_handler.getFontHandler().decreaseFonts()

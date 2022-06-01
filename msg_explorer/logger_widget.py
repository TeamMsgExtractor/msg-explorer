# This Python file uses the following encoding: utf-8
import logging

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from . import logger
from .ui.ui_logger_widget import Ui_LoggerWidget



class LoggerWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_LoggerWidget()
        self.ui.setupUi(self)

        self.__logger = logging.getLogger()
        self.__logger.addHandler(logger.WidgetLogger(self))
        self.__logger.setLevel(5)

    @Slot(str)
    def log(self, msg):
        """
        Add a message to the log, clearing space if necessary.
        """
        if self.ui.listLog.count() > 500:
            self.ui.listLog.takeItem(0)
        self.ui.listLog.addItem(msg)

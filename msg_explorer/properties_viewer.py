# This Python file uses the following encoding: utf-8
import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from . import utils
from .ui.ui_properties_viewer import Ui_PropertiesViewer


_DISPLAY_PROPS = (
    '0000',
    '0001',
    '0002',
    '0003',
    '0004',
    '0005',
    '0006',
    '0007',
    '000A',
    '000B',
    '0014',
    '0040',
    '0048',
    '00FB',
    '00FD',
    '00FE',
)


class PropertiesViewer(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_PropertiesViewer()
        self.ui.setupUi(self)

    @Slot()
    def clear(self):
        pass

    @Slot(extract_msg.Properties)
    def loadProperties(self, props):
        # We don't really need to load all of the properties,
        # so just load all of the relevant ones.
        self.ui.tableProps.clearContents()
        count = 0
        for prop in sorted(props.keys()):
            if prop[4:] in _DISPLAY_PROPS:
                count += 1
                self.ui.tableProps.setRowCount(count)
                self.ui.tableProps.setItem(count - 1, 0, QtWidgets.QTableWidgetItem(prop[:4]))
                self.ui.tableProps.setItem(count - 1, 1, QtWidgets.QTableWidgetItem(prop[4:]))
                self.ui.tableProps.setItem(count - 1, 2, QtWidgets.QTableWidgetItem(utils.dataToString(props[prop].value)))

# This Python file uses the following encoding: utf-8
import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT
from PySide6.QtWidgets import QTableWidgetItem

from . import utils
from .ui.ui_named_properties_viewer import Ui_NamedPropertiesViewer


class NamedPIDItem(QTableWidgetItem):
    """
    Little bit of a hack to force the Named PID column to sort properly.
    """
    def __lt__(self, item):
        return int(self.data(0)) < int(item.data(0))



class NamedPropertiesViewer(QtWidgets.QWidget):
    namedPropertySelected = Signal(list)
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_NamedPropertiesViewer()
        self.ui.setupUi(self)
        self.__msg = None

        self.ui.tableNamedProperties.cellDoubleClicked.connect(self._cellDoubleClicked)
        self.ui.comboBoxInstance.currentTextChanged.connect(self._comboBoxChanged)

    def loadNamed(self, namedInstance, attachment = None):
        """
        Load the named properties instance. If it is from an attachment,
        provide the instance so details can be acquired properly.
        """
        getStream = attachment._getTypedStream if attachment else self.__msg._getTypedStream
        named = namedInstance.namedProperties
        keys = sorted(named.keys())
        self.ui.tableNamedProperties.setRowCount(len(named))
        for index, key in enumerate(keys):
            self.ui.tableNamedProperties.setItem(index, 0, QTableWidgetItem(key))
            self.ui.tableNamedProperties.setItem(index, 1, NamedPIDItem(str(named[key].namedPropertyID)))
            # We need to figure out what to display for the data.
            if isinstance(named[key].data, (int, float, bool, None.__class__)):
                # This helps to shortcut a bunch of properties.
                self.ui.tableNamedProperties.setItem(index, 2, QTableWidgetItem(utils.dataToString(named[key].data)))
            elif isinstance(named[key].data, (bytes, list, tuple)) or getStream(f'__substg1.0_{0x8000 + named[key].namedPropertyID:04X}')[0]:
                self.ui.tableNamedProperties.setItem(index, 2, QTableWidgetItem('[Stream]'))
            else:
                self.ui.tableNamedProperties.setItem(index, 2, QTableWidgetItem(utils.dataToString(named[key].data)))

    @Slot()
    def msgClosed(self):
        self.ui.comboBoxInstance.clear()
        self.ui.tableNamedProperties.clearContents()
        self.__msg = None

    @Slot(extract_msg.MSGFile)
    def msgOpened(self, msgFile):
        self.__msg = msgFile
        self.ui.comboBoxInstance.addItem('MSG File')
        self.ui.comboBoxInstance.addItems((f'Attachment {x}' for x in range(len(msgFile.attachments))))
        self.loadNamed(msgFile.named)

    @Slot(int, int)
    def _cellDoubleClicked(self, row, column):
        if self.ui.tableNamedProperties.item(row, 2).data(0) == '[Stream]':
            name = self.ui.tableNamedProperties.item(row, 0).data(0)
            code = 0x8000 + int(self.ui.tableNamedProperties.item(row, 1).data(0))
            if self.ui.comboBoxInstance.currentText() == 'MSG File':
                start = ['']
            else:
                start [f'__attach_version1.0_#{int(self.ui.comboBoxInstance.currentText().split(" ")[1]):08X}', '']

            # Now we need to determine the type so we can generate the
            # path to give to the signal.
            for _type in extract_msg.constants.PTYPES:
                start[-1] = f'__substg1.0_{code:04X}{_type:04X}'
                if self.__msg.exists(start):
                    return self.namedPropertySelected.emit(start)
            else:
                QMessageBox.information(self, 'Notice', 'Stream for property was not found.')

    @Slot(str)
    def _comboBoxChanged(self, entry):
        if entry:
            if entry == 'MSG File':
                self.loadNamed(self.__msg.named)
            else:
                self.loadNamed(self.__msg.attachments[int(self.ui.comboBoxInstance.currentText().split(" ")[1])].namedProperties)




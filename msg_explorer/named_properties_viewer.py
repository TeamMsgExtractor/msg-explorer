# This Python file uses the following encoding: utf-8
import logging

import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem

from . import utils
from .ui.ui_named_properties_viewer import Ui_NamedPropertiesViewer


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
        self.__loading = False
        self.__msg = None
        # This is the named instance for the MSG file. It is used to get a list
        # of all available properties.
        self.__named : extract_msg.Named = None
        self.__attachments = None

        self.ui.tableNamedProperties.cellDoubleClicked.connect(self._cellDoubleClicked)
        self.ui.comboBoxInstance.currentTextChanged.connect(self._comboBoxChanged)

    def loadNamed(self):
        """
        Load the named properties instance. This loads the main sections for each
        property, not the data.
        """
        self.ui.tableNamedProperties.setRowCount(len(self.__named))
        self.ui.tableNamedProperties.setSortingEnabled(False)
        for index, key in enumerate(self.__named):
            self.ui.tableNamedProperties.setItem(index, 0, QTableWidgetItem(key))
            self.ui.tableNamedProperties.setItem(index, 1, NamedPIDItem(str(self.__named[key].namedPropertyID)))
        self.ui.tableNamedProperties.setSortingEnabled(True)

    @Slot()
    def msgClosed(self):
        self.ui.comboBoxInstance.clear()
        self.ui.tableNamedProperties.clearContents()
        self.ui.tableNamedProperties.setRowCount(0)
        self.__msg = None
        self.__named = None
        self.__attachments = None

    @Slot(extract_msg.MSGFile)
    def msgOpened(self, msgFile):
        self.__loading = True
        self.__msg = msgFile
        self.__named = msgFile.named
        self.__attachments = msgFile._rawAttachments if isinstance(msgFile, extract_msg.MessageSignedBase) else msgFile.attachments
        self.ui.comboBoxInstance.addItem('MSG File')
        self.ui.comboBoxInstance.addItems((f'Attachment {x}' for x in range(len(self.__attachments))))
        self.loadNamed()
        self.__loading = False
        self._comboBoxChanged('MSG File')

    @Slot(int, int)
    def _cellDoubleClicked(self, row, column):
        if self.ui.tableNamedProperties.item(row, 2).data(0) == '[Stream]':
            name = self.ui.tableNamedProperties.item(row, 0).data(0)
            code = 0x8000 + int(self.ui.tableNamedProperties.item(row, 1).data(0))
            if self.ui.comboBoxInstance.currentText() == 'MSG File':
                start = ['']
            else:
                start = [f'__attach_version1.0_#{int(self.ui.comboBoxInstance.currentText().split(" ")[1]):08X}', '']

            # Now we need to determine the type so we can generate the
            # path to give to the signal.
            for _type in extract_msg.constants.PTYPES:
                start[-1] = f'__substg1.0_{code:04X}{_type:04X}'
                logger.info(f'Checking for named property stream at {start}')
                if self.__msg.exists(start):
                    return self.namedPropertySelected.emit(start)
            else:
                QMessageBox.information(self, 'Notice', 'Stream for property was not found.')

    @Slot(str)
    def _comboBoxChanged(self, entry):
        # Prevent this from running while data is being loaded.
        if self.__loading:
            return
        if entry:
            if entry == 'MSG File':
                getData = self.__msg.namedProperties.get
                getStream = self.__msg._getTypedStream
            else:
                attachment = self.__attachments[int(entry.split(' ')[-1])]
                getData = attachment.namedProperties.get
                getStream = attachment._getTypedStream

            self.ui.tableNamedProperties.setSortingEnabled(False)
            for index in range(self.ui.tableNamedProperties.rowCount()):
                key = self.ui.tableNamedProperties.item(index, 0).data(0)
                # We need to figure out what to display for the data.
                data = getData(self.__named[key])
                if isinstance(data, (int, float, bool, None.__class__)):
                    # This helps to shortcut a bunch of properties.
                    self.ui.tableNamedProperties.setItem(index, 2, QTableWidgetItem(utils.dataToString(data)))
                elif isinstance(data, (bytes, list, tuple)) or getStream(f'__substg1.0_{self.__named[key].propertyStreamID}')[0]:
                    self.ui.tableNamedProperties.setItem(index, 2, QTableWidgetItem('[Stream]'))
                else:
                    self.ui.tableNamedProperties.setItem(index, 2, QTableWidgetItem(utils.dataToString(data)))
            self.ui.tableNamedProperties.setSortingEnabled(True)




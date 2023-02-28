# This Python file uses the following encoding: utf-8
import copy
import logging
import sys

import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from . import constants, utils
from .ui.ui_stream_viewer import Ui_StreamViewer


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class StreamViewer(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.ui = Ui_StreamViewer()
        self.ui.setupUi(self)
        self.__msg = None
        self.__dataViewerPage = None

        self.ui.buttonParsedView.toggled.connect(self._changeViewType)

        self.__currentPage = self.ui.pageParsedNoData

        self.__typePages = {
            'prop': self.ui.pageParsedProperties,
            '001E': self.ui.pageParsedString,
            '001F': self.ui.pageParsedString,
            '0048': self.ui.pageParsedGuidViewer,
            '0102': self.ui.pageHexViewer,
            '1002': self.ui.pageParsedMultiple,
            '1003': self.ui.pageParsedMultiple,
            '1004': self.ui.pageParsedMultiple,
            '1005': self.ui.pageParsedMultiple,
            '1006': self.ui.pageParsedMultiple,
            '1007': self.ui.pageParsedMultiple,
            '1014': self.ui.pageParsedMultiple,
            '101E': self.ui.pageParsedMultiple,
            '101F': self.ui.pageParsedMultiple,
            '1040': self.ui.pageParsedMultiple,
            '1048': self.ui.pageParsedMultiple,
            '1102': self.ui.pageParsedMultipleBinary,
        }

    @Slot()
    def _changeViewType(self):
        """
        Change the view type when the radio buttons are changed.
        """
        if self.ui.buttonParsedView.isChecked():
            self.ui.stackedWidget.setCurrentWidget(self.__currentPage)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageHexViewer)

    @Slot()
    def msgClosed(self):
        """
        Clean up the data when the msg file is closed.
        """
        self.__msg = None
        self.ui.labelStreamName.setText('None')
        self.ui.pageHexViewer.clear()
        if self.__currentPage != self.ui.pageParsedNoData:
            self.__currentPage.clear()
            self.__currentPage = self.ui.pageParsedNoData
        self._changeViewType()

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        self.__msg = msgFile

    @Slot(list)
    def openStream(self, name, prefix = True):
        """
        Loads the data for the specified stream. Will automatically
        determine how best to show it.
        """
        name = self.__msg.fixPath(name, prefix).split('/')
        # First thing is first, handle a multiple stream part being selected.
        if len(name[-1]) == 29:
            # A multiple stream part has 9 extra characters on the name. We are
            # just telling the function to run again with the main stream.
            return self.openStream(name[:-1] + [name[-1][:-9]])

        self.ui.pageHexViewer.loadHexData(self.__msg._getStream(name, False))
        # Make sure the path we use is local to the current file.
        self.ui.labelStreamName.setText('/'.join(name[self.__msg.prefixLen:]))
        # Now determine how to load the rest of the data.
        if name[-1] == '__properties_version1.0':
            _type = 'prop'
            source = self.__msg
            # Second part is to cut out the prefix for traversal.
            path = name[self.__msg.prefixLen:]
            # This is necessary for some operations.
            currentPath = []

            try:
                while len(path) > 1:
                    if path[0].startswith('__attach'):
                        source = source.attachments[int(path[0][-8:], 16)]
                    elif path[0].startswith('__recip'):
                        if isinstance(self.__msg, extract_msg.message_base.MessageBase):
                            # If it is a message base then the recipients already exist.
                            source = source.recipients[int(path[0][-8:], 16)]
                        else:
                            # Otherwise, they do not and we need to create one.
                            source = extract_msg.recipient.Recipient(currentPath + [path[0]], source)
                    elif path[0] == '__substg1.0_3701000D':
                        source = source.data
                    currentPath.append(path.pop(0))
            except Exception as e:
                utils.displayException(e)
                return
            props = source.props
            self.ui.pageParsedProperties.loadProperties(props)
        else:
            _type = name[-1][-4:]
            path = name[:-1] + [name[-1][:-4]]
            if constants.RE_STANDARD_FILE.match(name[-1]):
                data = self.__msg._getTypedStream(path, False, _type)[1]
                if _type in ('001E', '001F'): # String.
                    self.ui.pageParsedString.loadString(data, _type)
                elif _type == '0048': # GUID.
                    self.ui.pageParsedGuidViewer.loadGuid(data)
                elif _type == '0102': # Binary.
                    # For binary, we just show the hex viewer.
                    pass
                elif _type == '1102': # Multiple Binary.
                    # For multiple binary we load a page with a list
                    # of entries and a hex viewer that shows the
                    # currently selected one.
                    self.ui.pageParsedMultipleBinary.loadMultiple(data)
                elif _type.startswith('1'): # Other multiples.
                    self.ui.pageParsedMultiple.loadMultiple(data, _type)

        # First, check to make sure we are not opening a special custom attachment
        # file. If we are, this regular expression won't match it, and we just
        # treat it as binary data.
        if constants.RE_STANDARD_FILE.match(name[-1]):
            try:
                self.__currentPage = self.__typePages[_type]
            except KeyError as e:
                utils.displayException(e)
        else:
            logger.info(f'Attempting to view non-standard stream "{"/".join(name)}". Interpretting as plain binary data.')
            self.__currentPage = self.ui.pageHexViewer
        self._changeViewType()

    @Slot(str, bytes)
    def openStreamBytes(self, name : str, data : bytes):
        """
        Open a stream, overriding the behavior used for handling it. Used for
        displaying streams that are not accessible through normal means.
        """
        self.__currentPage = self.__typePages['0102']
        self.ui.labelStreamName = name
        self.ui.pageHexViewer.loadHexData(data)
        self._changeViewType()

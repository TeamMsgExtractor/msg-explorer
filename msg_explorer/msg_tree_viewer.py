# This Python file uses the following encoding: utf-8
import enum
import pprint

import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT
from PySide6.QtWidgets import QTreeWidgetItem

from . import utils
from .ui.ui_msg_tree_viewer import Ui_MSGTreeViewer


class _DataTypeEnum(enum.Enum):
    FILE = 0
    FOLDER = 1



class MsgTreeItem(QTreeWidgetItem):
    def __init__(self, text : str, _type : _DataTypeEnum):
        super().__init__((text,))
        self.__entryType = _type

    def __lt__(self, treeItem : "MsgTreeItem"):
        if self.__entryType == treeItem.__entryType:
            return self.data(0, 0) < treeItem.data(0, 0)
        else:
            # If they are not the same type, folder is always less than file.
            return self.__entryType == _DataTypeEnum.FOLDER

    @property
    def entryType(self) -> _DataTypeEnum:
        return self.__entryType



class MSGTreeViewer(QtWidgets.QWidget):
    # Signal to indicate a file has been double clicked.
    fileDoubleClicked = Signal(list)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.ui = Ui_MSGTreeViewer()
        self.ui.setupUi(self)

        self.iconProvider = QtWidgets.QFileIconProvider()

        self.ui.treeWidget.itemDoubleClicked.connect(self._treeItemDoubleClicked)
        self.ui.treeWidget.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

    @Slot()
    def msgClosed(self):
        self.ui.treeWidget.clear()

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        folderIcon = self.iconProvider.icon(QtWidgets.QFileIconProvider.Folder)
        fileIcon = fileIcon = self.iconProvider.icon(QtWidgets.QFileIconProvider.File)
        # First handle all of the storages. These will be the base
        # for all streams.
        storages = {}
        prefixLen = msgFile.prefixLen
        prefixTuple = tuple(msgFile.prefixList)
        for path in msgFile.listDir(False, True):
            # Only add if part of the local file.
            path = path[prefixLen:]
            storages[tuple(path)] = MsgTreeItem(path[-1], _DataTypeEnum.FOLDER)
            storages[tuple(path)].setIcon(0, folderIcon)

        # Now connect all of the parents together properly.
        for path in storages:
            if len(path) > 1:
                try:
                    parent = storages[path[:-1]]
                    parent.addChild(storages[path])
                except KeyError as e:
                    utils.displayException(e, 'Issue in MSG file detected: Storage directory exists but it\'s parent does not.')

        # Now add the top level ones to the tree.
        for path in storages:
            if len(path) == 1:
                self.ui.treeWidget.addTopLevelItem(storages[path])

        # Now we add the files.
        for path in msgFile.listDir(True, False):
            path = path[prefixLen:]
            item = MsgTreeItem(path[-1], _DataTypeEnum.FILE)
            item.setIcon(0, fileIcon)
            if len(path) > 1:
                try:
                    storages[tuple(path[:-1])].addChild(item)
                except KeyError as e:
                    utils.displayException(e, 'Issue in MSG file detected: stream exists but it\'s parent does not.')
            else:
                self.ui.treeWidget.addTopLevelItem(item)

    @Slot(QtWidgets.QTreeWidgetItem, int)
    def _treeItemDoubleClicked(self, item, column):
        """
        Handles a stream in the tree being double clicked.
        """
        # Check if the item clicked was a stream. If it was, then continue.
        if item.entryType == _DataTypeEnum.FILE:
            path = [item.data(0, 0)]
            while item.parent():
                item = item.parent()
                path.insert(0, item.data(0, 0))

            self.fileDoubleClicked.emit(path)




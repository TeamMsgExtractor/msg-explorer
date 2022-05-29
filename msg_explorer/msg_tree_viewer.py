# This Python file uses the following encoding: utf-8
import enum

import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from . import utils
from .ui.ui_msg_tree_viewer import Ui_MSGTreeViewer


class _DataTypeEnum(enum.Enum):
    FILE = 0
    FOLDER = 1

class MSGTreeViewer(QtWidgets.QWidget):
    # Signal to indicate a file has been double clicked.
    fileDoubleClicked = Signal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_MSGTreeViewer()
        self.ui.setupUi(self)

        self.iconProvider = QtWidgets.QFileIconProvider()

    @Slot()
    def msgClosed(self):
        pass

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        folderIcon = self.iconProvider.icon(QtWidgets.QFileIconProvider.Folder)
        fileIcon = fileIcon = self.iconProvider.icon(QtWidgets.QFileIconProvider.File)
        # First handle all of the storages. These will be the base
        # for all streams.
        self.ui.treeWidget.clear()
        storages = {}
        for path in msgFile.listDir(False, True):
            storages[tuple(path)] = QtWidgets.QTreeWidgetItem((path[-1],))
            storages[tuple(path)].setIcon(0, folderIcon)
            storages[tuple(path)].setData(0, 0x101, _DataTypeEnum.FOLDER)

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
            item = QtWidgets.QTreeWidgetItem((path[-1],))
            item.setIcon(0, fileIcon)
            item.setData(0, 0x101, _DataTypeEnum.FILE)
            if len(path) > 1:
                try:
                    storages[tuple(path[:-1])].addChild(item)
                except KeyError as e:
                    utils.displayException(e, 'Issue in MSG file detected: stream exists but it\'s parent does not.')
            else:
                self.ui.treeWidget.addTopLevelItem(item)



    Slot(QtWidgets.QTreeWidgetItem)
    def _treeItemDoubleClicked(self, item):
        # Check if the item clicked was a stream. If it was, then continue.
        if item.data(0, 0x101) == _DataTypeEnum.FILE:
            pass



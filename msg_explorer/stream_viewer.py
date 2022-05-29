# This Python file uses the following encoding: utf-8
import sys

import extract_msg

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, SIGNAL, Slot, SLOT

from .ui.ui_stream_viewer import Ui_StreamViewer


HEX_LINE_LEN = 0x10

_CHARS = [
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
    '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '.',
    '€', '.', '‚', 'ƒ', '„', '…', '†', '‡', 'ˆ', '‰', 'Š', '‹', 'Œ', '.', 'Ž', '.',
    '.', '‘', '’', '“', '”', '•', '–', '—', '˜', '™', 'š', '›', 'œ', '.', 'ž', 'Ÿ',
    ' ', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '.', '®', '¯',
    '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿',
    'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï',
    'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß',
    'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï',
    'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ',
]


class StreamViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_StreamViewer()
        self.ui.setupUi(self)
        self.__msg = None
        self.__dataViewerPage = None

    @Slot()
    def msgClosed(self):
        self.__msg = None

    @Slot(extract_msg.msg.MSGFile)
    def msgOpened(self, msgFile):
        self.__msg = msgFile

    @Slot(object)
    def openStream(self, name):
        """
        Loads the data for the specified stream. Will automatically
        determine how best to show it.
        """
        self.__loadHexData(self.__msg._getStream(name))


    def __loadHexData(self, data):
        # First we need to convert the bytes into a hex stream.
        hexStream = [f'{x:02X}' for x in data]
        lines = [hexStream[HEX_LINE_LEN * x: HEX_LINE_LEN * (x + 1)] for x in range((len(hexStream) + HEX_LINE_LEN - 1) // HEX_LINE_LEN)]
        rawDataLines = [data[HEX_LINE_LEN * x: HEX_LINE_LEN * (x + 1)] for x in range((len(data) + HEX_LINE_LEN - 1) // HEX_LINE_LEN)]

        # Process the raw data lines so they properly render. We want to
        # convert any bad characters into periods.
        rawDataLines = tuple(''.join(_CHARS[x] for x in line) for line in rawDataLines)


        # Pad out the last line if it is not 16 bytes.
        if lines:
            if len(lines[-1]) != 16:
                lines[-1] += ['  '] * (16 - len(lines[-1]))
        finalHexData = '\n'.join(' '.join(line) + '    ' + rawDataLines[index] for index, line in enumerate(lines))
        self.ui.hexViewer.setPlainText(finalHexData)

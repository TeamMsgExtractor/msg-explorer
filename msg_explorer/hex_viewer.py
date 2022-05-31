# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QFont

from . import font_handler
from .ui.ui_hex_viewer import Ui_HexViewer


HEX_LINE_LEN = 0x10

_CHARS = (
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
)


class HexViewer(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.ui = Ui_HexViewer()
        self.ui.setupUi(self)

        font_handler.getFontHandler().registerFont(self.ui.hexViewer.font, self.ui.hexViewer.setFont)

    @Slot()
    def clear(self):
        self.ui.hexViewer.setPlainText('')

    @Slot(bytes)
    def loadHexData(self, data):
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
        finalHexData = 'Offset    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F    Decoded Text\n'
        finalHexData += '\n'.join(f'{index:08X}  {" ".join(line)}    {rawDataLines[index]}' for index, line in enumerate(lines))
        self.ui.hexViewer.setPlainText(finalHexData)

from PySide6.QtCore import QObject, Slot


class _FontHandler(QObject):
    """
    Helper class to help with fonts so they can be globally increased
    or decreased.
    """
    def __init__(self):
        self.__fonts = []

    @Slot()
    def clearFonts():
        """
        Removes all fonts from the handler.
        """
        self.__fonts.clear()

    def registerFont(self, getter, setter):
        """
        Adds a font getter and setter function for the font to handle.
        """
        self.__fonts.append((getter, setter))

    @Slot()
    def increaseFonts(self, amount = 1):
        """
        Increases the fonts by the specified amount (default: 1).
        """
        for font in self.__fonts:
            newFont = font[0]()
            newFont.setPointSize(newFont.pointSize() + amount)
            font[1](newFont)

    @Slot()
    def decreaseFonts(self, amount = 1):
        """
        Decreases the fonts by the specified amount (default: 1).
        """
        for font in self.__fonts:
            newFont = font[0]()
            newFont.setPointSize(newFont.pointSize() - amount)
            font[1](newFont)



_fontHandler = _FontHandler()


def getFontHandler():
    """
    Gets the instance of the singleton FontHandler.
    """
    return _fontHandler

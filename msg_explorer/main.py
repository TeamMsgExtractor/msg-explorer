from .main_window import MainWindow

from PySide6.QtCore import QEventLoop
from PySide6.QtWidgets import QApplication



def mainRunner():
    app = QApplication([])
    from . import font_handler
    font_handler.getFontHandler().registerFont(QApplication.font, QApplication.setFont)

    widget = MainWindow()
    widget.show()

    font_handler.getFontHandler().increaseFonts(4)

    def runEventLoop():
        app.processEvents(QEventLoop.ExcludeUserInputEvents)

    widget.processEventLoop.connect(runEventLoop)

    return app.exec()

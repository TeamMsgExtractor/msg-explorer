from .main_window import MainWindow

from PySide6.QtCore import QEventLoop
from PySide6.QtWidgets import QApplication



def mainRunner():
    app = QApplication([])
    widget = MainWindow()
    widget.show()

    def runEventLoop():
        app.processEvents(QEventLoop.ExcludeUserInputEvents)

    widget.processEventLoop.connect(runEventLoop)

    return app.exec()

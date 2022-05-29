import traceback

from PySide6.QtWidgets import QDialog

from .ui.ui_unhandled_exception import Ui_UnhandledException


def getTracebackString(ex):
    """
    Takes the exception and returns a string of the formatted exception.
    """
    return ''.join(traceback.format_exception(ex.__class__, ex, ex.__traceback__))

def displayException(ex, alternateMessage = None):
    """
    Displays an unhandled exception in a new dialog.

    :param ex: The exception to display.
    :param alternateMessage: (Optional) An alternate message to put above
        the traceback.
    """
    dialog = QDialog()
    dialogUi = Ui_UnhandledException()
    dialogUi.setupUi(dialog)

    dialogUi.traceback.setPlainText(getTracebackString(ex))

    dialog.show()
    dialog.exec()

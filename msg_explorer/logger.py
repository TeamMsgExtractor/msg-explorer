import logging


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.__widget = widget
        self.setLevel(5)
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        """
        Actually handle logging the record.
        """
        try:
            msg = self.format(record)
            self.__widget.log(msg)
        except Exception:
            self.handleError(record)

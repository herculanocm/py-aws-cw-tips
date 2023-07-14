import logging

class RequestsHandlerCW(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        """Send the log records (created by loggers) to
        the appropriate destination.
        """
        print('Deu certo - ' + record.getMessage())
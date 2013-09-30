import logging
import traceback
from threading import Thread
from multiprocessing import Queue


class QueueHandler(logging.Handler):
    '''Logging handler that appends to a queue in main thread.
    '''

    def __init__(self):
        logging.Handler.__init__(self)

        self.q = Queue()

        self._handler = logging.StreamHandler()

        t = Thread(target=self._recv)
        t.daemon = True
        t.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(fmt)
        self._handler.setFormatter(fmt)

    def _recv(self):
        while True:
            try:
                record = self.q.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def emit(self, record):
        self.q.put_nowait(record)
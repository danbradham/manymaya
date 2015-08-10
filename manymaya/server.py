from multiprocessing import managers
from Queue import Queue, Empty
from manymaya.logger import logger
import time

result_q = Queue()
task_q = Queue()


def get_result_q():
    return result_q


def get_task_q():
    return task_q


class ServerManager(managers.SyncManager):
    pass

ServerManager.register("get_result_q", get_result_q)
ServerManager.register("get_task_q", get_result_q)


class Server(object):

    def __init__(self, port, authkey):
        self.manager = server_manager(port, authkey)
        self.result_q = self.manager.get_result_q()
        self.task_q = self.manager.get_task_q()

        logger.info("ManyMaya Server started on port {0}".format(port))

    def start(self):
        while True:
            while not self.result_q.empty():
                task = self.result_q.get()
                if task.exc:
                    logger.exception(task.result)
                else:
                    logger.info(task.result)
            time.sleep(1)


def server_manager(port, authkey):
    '''Starts and returns a multiprocessing.Manager with a task queue and
    result queue.
    '''

    manager = ServerManager(address=('localhost', port), authkey=authkey)
    manager.start()
    return manager

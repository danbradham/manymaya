from multiprocessing import managers, Process
from manymaya.logger import logger
from manymaya.tasks import Task


class ClientManager(managers.SyncManager):
    '''Base Client Manager'''

ClientManager.register("get_task_q")
ClientManager.register("get_result_q")


class Client(object):

    def __init__(self, ip, port, authkey, processes=0):
        self.manager = client_manager(ip, port, authkey)
        logger.info("ManyMaya Client connected to {0}:{1}.".format(ip, port))

        self.task_q = self.manager.get_task_q()
        self.result_q = self.manager.get_result_q()
        self.procs = []

        if processes:
            from manymaya.worker import worker
            for i in xrange(processes):
                p = Process(target=worker, args=(self.task_q, self.result_q))
                self.procs.append(p)
                p.start()


    def start(self):

        for p in self.procs:
            p.join()

    def submit(self, task):
        if not isinstance(task, Task):
            raise TypeError("Tasks must be a subclass of manymaya.tasks.Task")
        task.queued = True
        self.task_q.put(task)


def client_manager(ip, port, authkey):
    '''Starts and returns a client connected to port and authkey.'''

    manager = ClientManager(address=(ip, port), authkey=authkey)
    manager.connect()
    return manager

import time
from Queue import Empty
from functools import partial
import maya.standalone as standalone

maya = partial(standalone.initialize, name="python")


def worker(task_q, result_q):
    '''Maya worker!'''
    from manymaya.logger import logger
    #Start maya standalone
    logger.info("Worker Initialized")
    #maya()

    while True:
        try:
            task = task_q.get_nowait()
            # logger.info("Task Found: {name} Active".format(**task.__dict__))
            result_q.put(task())
        except Empty:
            time.sleep(1)

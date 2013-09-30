import logging
logger = logging.getLogger('ManyMaya')
import os
import sys
from multiprocessing import cpu_count, Process, Queue
from functools import wraps
from .queuehandler import QueueHandler
import maya.standalone


def instance(fn):
    '''Wraps a function in a maya.standalone process.

    :param fn: The decorated function.
    :param queue : The file queue.
    '''

    @wraps(fn)
    def wrapped(queue):
        logger.info('Starting Process')
        maya.standalone.initialize(name='python')
        while not queue.empty():
            f = queue.get()
            try:
                fn(f)
            except Exception, e:
                raise Exception(e)
        logger.info('Finishing Process')
        logger.info('HELLO')
        sys.stdout.flush()
    return wrapped


def find(inside, exts=['ma', 'mb'], subdirs=True):
    '''Search a specified directory for Maya compatible files.
    Returns a list of filepaths for use with :function <start>:.

    :param inside: Path to search.
    :param ma: Include *.ma files in return (optional)
    :param mb: Include *.mb files in return (optional)
    :param subdirs: Search inside subdirs. (optional)
    '''

    maya_files = []
    for d, s, files in os.walk(inside):
        for f in files:
            if f.split('.')[-1] in exts:
                maya_files.append(os.path.abspath(os.path.join(d, f)))

    return maya_files


def start(file_list, fn, processes=4, verbose=False):
    '''Create a multiprocess pool.

    :param file_list: List of files to process.
    :param fn: Target function.
    :param processes: Number of processes to run concurrently.(optional)
    '''

    qhandler = QueueHandler()
    logger.addHandler(qhandler)
    if verbose:
        qhandler.setLevel(logging.INFO)
    else:
        qhandler.setLevel(logging.WARNING)

    cpus = cpu_count()
    processes = processes if processes else cpus

    q = Queue()
    for f in file_list:
        q.put(f)

    workers = [Process(target=fn, args=(q,)) for i in range(processes)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

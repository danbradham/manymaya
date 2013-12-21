import functools
import os
import sys
import logging
from multiprocessing import cpu_count, Process, Queue
from .logger import logger
import maya.standalone


def log(message, level="INFO"):
    '''Fluff...Exists only to shorten logging calls for the end user.

    :param message: Message to log.
    :param level: Level at which to log message.(optional)
    '''

    {"DEBUG": logger.debug,
     "INFO": logger.info,
     "WARNING": logger.warning,
     "ERROR": logger.error,
     "CRITICAL": logger.critical}[level](message)


def find(inside, exts=['ma', 'mb'], subdirs=True):
    '''Search a specified directory for Maya compatible files.
    Returns a list of filepaths for use with :function <start>:.

    :param inside: Path to search.
    :param exts: Extensions of files to include in returned list. (optional)
    :param subdirs: Search inside subdirs. (optional)
    '''

    matched_files = []
    for d, s, files in os.walk(inside):
        for f in files:
            if f.split('.')[-1] in exts:
                matched_files.append(os.path.abspath(os.path.join(d, f)))

    return matched_files


def instance(fn):
    '''A decorator that wraps your function inside a maya.standalone
    instance and injects a file queue.

    :param fn: The decorated function.
    '''

    @functools.wraps(fn)
    def inst_wrapper(queue):
        '''Pre and post setup for maya.standalone instance.

        :param queue: The file queue.
        '''

        maya.standalone.initialize(name='python')
        while not queue.empty():
            f = queue.get()
            try:
                fn(f)
            except Exception, e:
                logger.error(e)
    return inst_wrapper


def start(file_list, fn, processes=0, verbose=False):
    '''Creates a multiprocessing Queue from and run several worker
    processes to pull from it.

    :param file_list: List of files to process.
    :param fn: Target function.
    :param processes: Number of processes to run concurrently.(optional)
    :param verbose: Enable/Disable verbose output.(optional)
    '''

    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    cpus = cpu_count()
    processes = processes if processes and processes <= cpus else cpus

    q = Queue()
    for f in file_list:
        q.put(f)

    workers = [Process(target=fn, args=(q,)) for i in range(processes)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

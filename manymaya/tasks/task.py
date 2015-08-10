import abc
from timeit import default_timer
import traceback


def format_time(h, m, s):
    if h:
        return "{0}h {1}m".format(h, m)
    if m:
        return "{0}m {1}s".format(m, s)
    if s:
        return "{0:.2f}s".format(s)


class Progress(object):

    def __init__(self):
        self.step = 1
        self.maximum = 100
        self.current_step = 0
        self.start_time = None

    def start(self):
        self.start_time = default_timer()

    def next(self):
        if not self.completed:
            self.current_step += self.step
            if self.completed:
                self.end_time = default_timer()

    @property
    def completed(self):
        return True if self.current_step == self.maximum else False

    @property
    def time_left(self):
        elapsed = default_timer() - self.start_time
        try:
            tl = ((elapsed / self.current_step)
                  * (self.maximum - self.current_step))
        except ZeroDivisionError:
            return (99, 99, 99)
        minutes, seconds = divmod(tl, 60.0)
        hours, minutes = divmod(minutes, 60.0)
        return hours, minutes, seconds

    def format_time_left(self):
        return format_time(*self.time_left)

    @property
    def time_elapsed(self):
        elapsed = default_timer() - self.start_time
        minutes, seconds = divmod(elapsed, 60.0)
        hours, minutes = divmod(minutes, 60.0)
        return hours, minutes, seconds

    def format_time_elapsed(self):
        return format_time(*self.time_elapsed)

    @property
    def percent(self):
        return (self.current_step / float(self.maximum)) * 100

    def format_percent(self):
        return "{0:.2f}%".format(self.percent)


class Task(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.queued = False
        self.active = False
        self.completed = False
        self.result = None
        self.exc = None
        self.progress = Progress()

    def __call__(self):
        self.queued = False
        self.active = True

        try:
            self.result = self.run(*self.args, **self.kwargs)
            self.completed = True
        except:
            self.exc = True
            self.result = traceback.format_exc()

        self.active = False
        return self

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        '''The function that will run inside of maya.'''
        return

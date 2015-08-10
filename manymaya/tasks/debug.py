from manymaya.tasks import Task

class Debug(Task):

    def run(self, *args, **kwargs):
        return args, kwargs

'''
Test manymaya.task.Task
'''

from manymaya.task import Task, Progress


class DivTask(Task):

    def run(self, a, b):
        return a/b


class SumTask(Task):

    def run(self, items):
        num_items = len(items)
        self.progress.maximum = num_items
        self.progress.start()

        total = items[0]
        for item in items[1:]:
            total += item
            self.progress.next()

        return total


def test_exc():

    task = DivTask("ZeroDivision Task", 5, 0)
    task()

    assert task.exc
    assert not task.completed
    assert "ZeroDivisionError" in task.result


def test_success():

    items = range(20)
    task = SumTask("Sum List Task", range(20))
    task()

    assert not task.exc
    assert task.result == sum(items)
    assert task.completed


def test_progress():

    num_items = 20
    items = xrange(num_items)

    p = Progress()
    p.maximum = num_items
    p.start()

    for item in items:
        percent = (item / float(num_items)) * 100
        assert p.percent == percent
        assert p.format_percent() == "{0:.2f}%".format(percent)
        p.next()

    assert p.completed

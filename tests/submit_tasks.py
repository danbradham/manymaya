#!/usr/autodesk/maya2014-x64/bin/mayapy
from manymaya.client import Client
from manymaya.tasks.debug import Debug

if __name__ == "__main__":
    cli = Client(
        "localhost",
        8081,
        authkey="test_key",
        )

    for i in xrange(20):
        cli.submit(Debug("DebugTask {0}".format(i), tid=i))

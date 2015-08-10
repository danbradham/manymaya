#!/usr/autodesk/maya2014-x64/bin/mayapy
from manymaya.client import Client
from manymaya.logger import logger

if __name__ == "__main__":
    Client(
        "localhost",
        8081,
        authkey="test_key",
        processes=4
        ).start()

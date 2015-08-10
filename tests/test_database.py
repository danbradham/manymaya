'''
Let's test our tiny wrapper.
'''

import manymaya.database as mmdb
import os
from nose.tools import with_setup
from functools import partial


test_data = partial(os.path.join, os.path.dirname(__file__), "data")
cfg_file = test_data("example-config.json")
db_name = test_data("example.db")
db_schema = test_data("example_schema.sql")


def clean_start():
    if os.path.exists(db_name):
        os.remove(db_name)


@with_setup(clean_start)
def test_context():
    with mmdb.connect(cfg_file) as c:
        assert c.db_name == db_name
        assert c.db_schema == db_schema

    assert os.path.exists(db_name)

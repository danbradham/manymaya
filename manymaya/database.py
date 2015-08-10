import contextlib
import json
import sqlite3
import os


class Database(object):

    def __init__(self, config):
        with open(config) as f:
            cfg = json.loads(f.read())
        try:
            self.db_name = cfg["db_name"]
            self.db_schema = cfg["db_schema"]
        except KeyError:
            raise KeyError(
                "Your config file must contain db_name and db_schema keys")

        self.conn = None

    def connect(self):
        db_exists = os.path.exists(self.db_name)
        self.conn = sqlite3.connect(self.db_name,
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

        if not db_exists:
            with open(self.db_schema) as f:
                schema = f.read()

            self.conn.executescript(schema)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def execute(self, cmd):
        self.conn.execute(cmd)


@contextlib.contextmanager
def connect(config):
    db = Database(config)
    try:
        db.connect()
        yield db
    except Exception, err:
        print "Error: ", err
        db.rollback()
    finally:
        db.commit()
        db.close()

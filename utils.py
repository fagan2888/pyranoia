from sqlite3 import connection, IntegrityError

class DBConnection(object):

    def __init__(self, db_name):
        self._db = db_name

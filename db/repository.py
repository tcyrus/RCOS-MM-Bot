import psycopg2

class PostgresRepository(object):
    def __init__(self):
        # ToDo use connection config
        self.client = psycopg2.connect("")

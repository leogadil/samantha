import sqlite3
import os
from .helper import uuid, create_folder

class column:
    def __init__(self, name, type, primary_key=False, auto_increment=False, not_null=False, unique=False, default=None):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.not_null = not_null
        self.unique = unique
        self.default = default

    def __str__(self):
        return '{} {}'.format(self.name, self.type)

class database:
    def __init__(self, db_path):
        create_folder(os.path.abspath('.') + db_path)
        _id = uuid()
        self.db_name = "{}{}{}.db".format(os.path.abspath('.'),db_path, _id)
        self.db_connection = None
        self.db_cursor = None

    def connect(self):
        self.db_connection = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connection.cursor()

    def disconnect(self):
        self.db_connection.close()

    def execute(self, query, args=None):
        if args is None:
            self.db_cursor.execute(query)
        else:
            self.db_cursor.execute(query, args)

    def commit(self):
        self.db_connection.commit()

class ActiveDatabase(database):
    def __init__(self, cls):
        super().__init__('/data/repository/active/{}/'.format(cls.__class__.__name__))
        print('Creating database: {}'.format(self.db_name))
        self.connect()

    def create_table(self, table_name, columns):
        query = 'CREATE TABLE IF NOT EXISTS {} ('.format(table_name)
        for column in columns:
            query += '{} {}'.format(column.name, column.type)
            if column.primary_key:
                query += ' PRIMARY KEY'
            if column.auto_increment:
                query += ' AUTOINCREMENT'
            if column.not_null:
                query += ' NOT NULL'
            if column.unique:
                query += ' UNIQUE'
            if column.default is not None:
                query += ' DEFAULT {}'.format(column.default)
            query += ', '
        query = query[:-2] + ')'
        print(query)
        self.execute(query)

    def __del__(self):
        if self.db_connection is not None:
            self.disconnect()
            print('Deleting database: {}'.format(self.db_name))
            os.remove(self.db_name)
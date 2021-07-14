import sqlite3

class Database:
    def __init__(self, database: str):
        self.database = database
        self._database = None

    @property
    def db(self):
        database = self._database

        if database is None:
            database = self._database = sqlite3.connect(self.database)
        
        return database

    def close(self):
        database = self._database

        if database is not None:
            database.close()

    def query_db(self, query: str, args=(), one=False):
        cur = self.db.execute(query, args)
        rv = cur.fetchall()
        self.db.commit()
        cur.close()

        return (rv[0] if rv else None) if one else rv

    def query_dict(self, query: str, args=(), one=False):
        database = self.db

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]

            return d

        database.row_factory = dict_factory 
        c = database.execute(query, args)
        r = c.fetchall()
        database.commit()

        return (r[0] if r else None) if one else r

    def insert(self, table: str, data: dict):
        query = f"INSERT into \"{table}\" ({', '.join(data.keys())}) VALUES ({', '.join(['?'] * len(data.keys()))})"
        return self.query_dict(query, tuple(data.values()))

    def insert_multiple(self, table: str, columns: tuple, values: tuple):
        query = f"INSERT into \"{table}\" ({', '.join(columns)}) VALUES"
        _values = []

        for value in values:
            query += f" ({', '.join(['?'] * len(value))}),"
            _values += value

        query = query[0:-1]
        return self.query_dict(query, tuple(_values))

    def update(self, table: str, data: dict, where: dict = {}):
        query = f"UPDATE \"{table}\" SET {' = ?,'.join(data.keys())} = ?"

        if where is not None and len(where) > 0:
            query += f" WHERE {'? '.join(where.keys())}?"

        return self.query_dict(query, tuple(list(data.values()) + list(where.values())))

    def delete(self, table: str, where: dict = {}):
        query = f"DELETE FROM \"{table}\""

        if where is not None and len(where) > 0:
            query += f" WHERE {'? '.join(where.keys())}?"

        return self.query_dict(query, tuple(list(where.values())))

    def select(self, table: str, columns: tuple = ('*'), where: dict = {}, one=False):
        query = f"SELECT {', '.join(columns)} FROM \"{table}\""

        if where is not None and len(where) > 0:
            query += f" WHERE {'? '.join(where.keys())}?"

        return self.query_dict(query, tuple(where.values()), one)

    def exists(self, table: str, where: dict = {}):
        query = f"SELECT * FROM \"{table}\""

        if where is not None and len(where) > 0:
            query += f" WHERE {'? '.join(where.keys())}?"

        result = self.query_dict(query, tuple(where.values()))

        return result and len(result) > 0

    def create_table(self, table: str, columns: dict):
        query = f"CREATE TABLE \"{table}\" ("

        for c in columns:
            query += f' {c} {columns[c]},'

        query = query[0: -1] + " );"
        return self.query_dict(query)

    def drop_table(self, table: str):
        return self.query_dict(f"DROP TABLE \"{table}\"")
import cx_Oracle


class Database:
    def __init__(self, user: str, password: str, dsn: str):
        cx_Oracle.init_oracle_client(lib_dir="C:\oracle\instantclient_21_3")

        self.conn = cx_Oracle.connect(user, password, dsn)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def fetch_all(self, table: str, additional: str = '') -> list[tuple[str]]:
        self.cur.execute(f'SELECT * FROM {table} {additional}')
        return self.cur.fetchall()

    def insert(self, table: str, values: tuple):
        sql = f'INSERT INTO {table} VALUES {values}'.replace('None', 'NULL')
        self.cur.execute(sql)
        self.conn.commit()

    def remove(self, table: str, additional: str):
        self.cur.execute(f'DELETE FROM {table} WHERE {additional}')
        self.conn.commit()

    def update(self, table: str, additional: str):
        self.cur.execute(f'UPDATE {table} SET {additional}')
        self.conn.commit()

import logging

create_table_command = '''CREATE TABLE IF NOT EXISTS {}(
Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
UserId BIGINT NOT NULL UNIQUE,
UserName STRING NOT NULL,
RegDateTime DATETIME NOT NULL,
UserEmail TEXT,
PhoneNumber VARCHAR(12),
PassDate DATE,
Balance INTEGER NOT NULL DEFAULT 0,
Referral INTEGER
);'''

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

import sqlite3
from datetime import datetime


class SQLWorker:
    """

    :param database: databases name <example.db> or <:memory:> to save bd in RAM
    :type database: str
    """

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        logging.info('Connection to databases')
        self.cursor = self.connection.cursor()

    def request(self, req: str, *args) -> sqlite3.Cursor:
        """SQL Запрос

        :param req: sql request
        :type req: str
        :rtype: sqlite3.Cursor
        """
        with self.connection:
            return self.cursor.execute(req, *args)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

    def __del__(self):
        self.close()


class BotSQL(SQLWorker):
    """

    :param database: databases name <example.db> or <:memory:> to save bd in RAM
    :type database: str
    :param table_name: name of table
    :type table_name: str
    """
    BUFFER = ':memory:'

    def __init__(self, database: str, table_name: str):
        super().__init__(database)
        self.table_name = table_name

    def create_table(self):
        """Создает таблицу"""
        with self.connection:
            self.cursor.execute(create_table_command.format(self.table_name))

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute(f'SELECT * FROM {self.table_name}').fetchall()

    def select_3_usernames(self):
        with self.connection:
            return self.cursor.execute(f'SELECT UserId, UserName FROM {self.table_name} LIMIT 3').fetchall()

    def add_new_user(self, user_id: int, user_name: str, user_firstname: str, user_surname: str, *,
                     referral: int = None):

        if referral:
            self.request(
                f'INSERT INTO {self.table_name}(UserId, UserName, RegDateTime, PassDate, Referral) '
                f'VALUES(?, ?, CURRENT_TIMESTAMP, \'2008-01-01\', ?);',
                (user_id, user_name, referral))
        else:
            self.request(
                f'INSERT INTO {self.table_name}(UserId, UserName, RegDateTime, PassDate) '
                f'VALUES(?, ?, CURRENT_TIMESTAMP, \'2008-01-01\');',
                (user_id, user_name))

    def update_user_data(self, user_id: int, field: str, value):
        """

        :param user_id: id user
        :param field: name of field in table to update
        :param value: value
        """
        self.request(f'UPDATE {self.table_name} SET {field} = {value} WHERE UserID = {user_id}')

    def get_user_data(self, user_id: int) -> tuple:
        """

        :param user_id: id user
        :return: tuple of fields in db table
        :rtype: tuple
        """
        return self.request(f"SELECT * FROM Users WHERE UserId={user_id}").fetchone()

    def update_passdate(self, user_id: int):
        self.update_user_data(user_id, 'PassDate', 'CURRENT_DATE')

    def get_passdate_days(self, user_id):
        passdate = self.request(f"SELECT PassDate FROM {self.table_name} WHERE UserId={user_id}").fetchone()[0]
        now = datetime.now()
        deadline = datetime(*map(int, passdate.split('-')))
        return (now - deadline).days

    def is_passdate_expired(self, user_id):
        return self.get_passdate_days(user_id) > 30

    def get_user_balance(self, user_id):
        return self.request(f'SELECT Balance FROM {self.table_name} WHERE UserId={user_id}').fetchone()[0]

    def update_user_balance(self, user_id, money):
        return self.request(f'UPDATE {self.table_name} SET Balance=Balance+{float(money)} WHERE UserId = {user_id}')

    def get_users_count(self):
        return self.request(f"SELECT COUNT(*) FROM {self.table_name}").fetchone()[0]

    def get_top_3_by_balance(self):
        return self.request(f'SELECT UserId, UserName, Balance FROM {self.table_name} ORDER BY Balance DESC LIMIT 3') \
            .fetchall()

    def check_referrals(self, user_id):
        return self.request(f"SELECT UserName FROM {self.table_name} WHERE Referral="
                            f"(SELECT UserId FROM {self.table_name} WHERE UserId={user_id})").fetchone()

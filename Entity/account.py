import mysql.connector
class Account:
    def __init__(self):
        self.mydb = self.connectToDatabase()

    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321",
            auth_plugin='mysql_native_password'
        )

    def fetchOne(self, sql, val) -> dict:
        with self.mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchone()
        return result

    def fetchAll(self, sql, val) -> list:
        with self.mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchall()
        return result

    def commit(self, sql, val):
        with self.mydb.cursor() as cursor:
            cursor.execute(sql, val)
            self.mydb.commit()
            return cursor.lastrowid
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()

    def insert_account(self):
        pass

    def get_account(self):
        pass
import mysql.connector
from datetime import datetime, timedelta
class EmailVerification:
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

    def emailVerify(self, email, code) -> None or Exception:
        sql = "SELECT * FROM emailVerification WHERE email=%s AND code=%s"
        val = (email, code)
        record = self.fetchOne(sql, val)
        if record is None:
            raise Exception("Invalid code, please send and enter again")

        verification_date = record['verificationDate']
        if datetime.now() - verification_date > timedelta(minutes=5):
            raise Exception("The verification code has expired, please request a new one")

    def insert_verify_code(self, email, code):
        sql = "INSERT INTO emailVerification (email, code) VALUES (%s, %s)"
        val = (email, code)
        self.commit(sql, val)

if __name__ == "__main__":
    EmailVerification().insert_verify_code("<EMAIL>", "1")

import mysql.connector
class Review:
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
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()

    def get_all_reviews(self):
        sql = "SELECT * FROM review JOIN account on review.accountId = account.accountId"
        return self.fetchAll(sql,"")

    def get_all_HeadLine_reviews(self):
        sql = "SELECT * FROM review LEFT JOIN account ON review.accountId = account.accountId WHERE isHeadline = 1"
        return self.fetchAll(sql,"")
    def insert_review_by_id(self, accountId,rating,reviewText):
        sql = "INSERT INTO review (accountId,rating,reviewText) VALUES (%s,%s,%s)"
        val = (accountId,rating,reviewText)
        self.commit(sql,val)

    def headline_review_by_id(self,reviewId):
        sql = "UPDATE review SET isHeadline= 1 WHERE reviewId=%s"
        val = (reviewId,)
        self.commit(sql,val)

    def delete_review_by_id(self,reviewId):
        sql = "DELETE FROM review WHERE reviewId=%s"
        val = (reviewId,)
        self.commit(sql,val)

if __name__ == "__main__":
    review = Review()
    print(review.delete_review_by_id("2"))
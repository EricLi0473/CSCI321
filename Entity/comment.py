import mysql.connector

class Comment:
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
    def get_comments_by_symbol(self,symbol):
        sql = "select comment.commentId,account.accountId,account.userName,comment.commentText,comment.commentDate, comment.likes, comment.dislikes from comment left join account on comment.accountId = account.accountId where stockSymbol=%s"
        result = self.fetchAll(sql, (symbol,))
        return result

    def insert_comment(self, accountId, symbol,comment):
        sql = "insert into comment (accountId,stockSymbol,commentText) values (%s,%s,%s)"
        self.commit(sql, (accountId,symbol,comment))

    def delete_comment_by_id(self, commentId):
        sql = "delete from comment where commentId=%s"
        self.commit(sql, (commentId,))

    def update_comment_likes(self, commentId):
        sql = "update comment set likes = likes + 1 where commentId=%s"
        self.commit(sql, (commentId,))

    def update_comment_dislikes(self, commentId):
        sql = "update comment set dislikes = dislikes + 1 where commentId=%s"
        self.commit(sql, (commentId,))

if __name__ == '__main__':
    print(Comment().get_comments_by_symbol("aapl"))
    Comment().get_comments_by_symbol("aapl")

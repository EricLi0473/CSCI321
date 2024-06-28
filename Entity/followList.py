import mysql.connector
class FollowList():
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

    def fetchOne(self, sql, val,dictionary=True) -> dict:
        with self.mydb.cursor(dictionary=dictionary) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchone()
        return result

    def fetchAll(self, sql, val,dictionary=True) -> list:
        with self.mydb.cursor(dictionary=dictionary) as cursor:
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

    def insert_followList_by_id(self,accountId,followedId):
        sql = "INSERT INTO followList (accountId,followedId,notifyMe) VALUES (%s,%s,0)"
        val = (accountId,followedId)
        self.commit(sql,val)

    def remove_follower_in_followList_by_id(self,accountId,followedId):
        sql = "DELETE FROM followList WHERE accountId=%s AND followedId=%s"
        val = (accountId,followedId)
        self.commit(sql,val)

    def get_account(self):
        pass

    def get_followList_by_accountId(self,accountId):
        sql = """
        SELECT followList.followId, followList.accountId AS followListAccountId, followList.followedId, followList.notifyMe, followList.followDate, 
               account.accountId AS accountAccountId, account.userName, account.hashedPassword, account.email, account.bio, account.profile, 
               account.status, account.createDateTime, account.age, account.sex, account.occupation, account.incomeLevel, account.netWorth, 
               account.investmentExperience, account.riskTolerance, account.investmentGoals
        FROM followList
        LEFT JOIN account ON followList.followedId = account.accountId
        WHERE followList.accountId = %s
        """
        val = (accountId,)
        return self.fetchAll(sql, val)

    #this function use for threshold update
    def get_accountList_by_followedId(self,followedId):
        sql = """
        SELECT followList.followId, followList.accountId AS followListAccountId, followList.followedId, followList.notifyMe, followList.followDate, 
               account.accountId AS accountAccountId, account.userName, account.hashedPassword, account.email, account.bio, account.profile, 
               account.status, account.createDateTime, account.age, account.sex, account.occupation, account.incomeLevel, account.netWorth, 
               account.investmentExperience, account.riskTolerance, account.investmentGoals
        FROM followList
        LEFT JOIN account ON followList.followedId = account.accountId
        WHERE followList.followedId = %s
        """
        val = (followedId,)
        return self.fetchAll(sql, val)

    #this function use for get who follows me
    def get_who_follows_me_by_accountID(self,followedId):
        sql = """
        SELECT followList.followId, followList.accountId AS followListAccountId, followList.followedId, followList.notifyMe, followList.followDate, 
               account.accountId AS accountAccountId, account.userName, account.hashedPassword, account.email, account.bio, account.profile, 
               account.status, account.createDateTime, account.age, account.sex, account.occupation, account.incomeLevel, account.netWorth, 
               account.investmentExperience, account.riskTolerance, account.investmentGoals
        FROM followList
        LEFT JOIN account ON followList.accountId = account.accountId
        WHERE followList.followedId = %s
        """
        val = (followedId,)
        return self.fetchAll(sql, val)

    def get_notifyMe_value_from_accountAndFollowId(self,accountId,followedId) ->int:
        sql = "SELECT notifyMe FROM followList WHERE accountId = %s AND followedId = %s"
        val = (accountId,followedId,)
        return self.fetchOne(sql, val)["notifyMe"]

if __name__ == "__main__":
    FollowList().remove_follower_in_followList_by_id("1","3")
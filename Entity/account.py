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

    def insert_account(self):
        pass

    def get_account(self):
        pass

    def get_premium_accountId(self) -> tuple:
        sql = "SELECT accountId FROM account WHERE profile = 'premium'"
        list = []
        for id in self.fetchAll(sql,""):
            list.append(id['accountId'])
        return list

    def get_account_by_accountId(self,accountId) -> dict:
        sql = "select * from account where accountId = %s"
        val = (accountId,)
        return self.fetchOne(sql,val)

    def get_all_account(self):
        sql = "select * from account"
        return self.fetchAll(sql,"")

    def get_accounts_by_userName(self, userName, accountId) -> list[dict]:
        if not userName:
            return []
        sql = "SELECT * FROM account WHERE userName LIKE %s AND accountId != %s"

        results = self.fetchAll(sql, (f"{userName}%",accountId))
        return results

    def update_password_by_accountId(self, accountId, hashedPassword) -> str or Exception:
        try:
            sql = "UPDATE account SET hashedPassword = %s WHERE accountId = %s"
            val = (hashedPassword, accountId)
            self.commit(sql, val)
            return hashedPassword
        except Exception as e:
            raise Exception(e)

    def verifyAccount(self, email, HashPassword) -> dict or Exception:
        sql = "SELECT * FROM account WHERE email = %s"
        result = self.fetchOne(sql, (email,))
        if result:
            if result['status'] == 'invalid':
                raise Exception("Your account has been banned.")
            elif result['hashedPassword'] == HashPassword:
                return result
            else:
                raise Exception("Incorrect password")
        else:
            raise Exception("Account does not exist")
    def update_profile_status(self,accountId,status):
        sql = "UPDATE account SET status = %s WHERE accountId = %s"
        val = (status,accountId)
        return self.commit(sql,val)

    def update_Account(self, accountId, userName, email, bio, age, sex, occupation, incomeLevel, netWorth,
                             investmentExperience, riskTolerance, investmentGoals, profile,isPrivateAccount,mlViewLeft) -> bool:
        sql = """
        UPDATE account
        SET userName = %s,
            email = %s,
            bio = %s,
            age = %s,
            sex = %s,
            occupation = %s,
            incomeLevel = %s,
            netWorth = %s,
            investmentExperience = %s,
            riskTolerance = %s,
            investmentGoals = %s,
            profile = %s,
            isPrivateAccount = %s,
            mlViewLeft = %s
        WHERE accountId = %s
        """
        values = (
        userName, email, bio, age, sex, occupation, incomeLevel, netWorth, investmentExperience, riskTolerance,
        investmentGoals, profile, isPrivateAccount,mlViewLeft,accountId)

        try:
            self.commit(sql, values)
            return True
        except Exception as e:
            print(f"Error updating personal info: {e}")
            return False

    def signUp(self, userName, hashedPassword, email, profile, age, sex, occupation, incomeLevel, netWorth,
               investmentExperience, riskTolerance, investmentGoals) -> dict:

        sql = """
        INSERT INTO account 
        (userName, hashedPassword, email, profile, age, sex, occupation, incomeLevel, netWorth, investmentExperience, riskTolerance, investmentGoals) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s)
        """
        val = (userName, hashedPassword, email, profile, age, sex, occupation, incomeLevel, netWorth,
                        investmentExperience, riskTolerance, investmentGoals)

        lastId = self.commit(sql, val)
        sql = 'SELECT * FROM account WHERE accountId = %s'
        val = (lastId,)
        return self.fetchOne(sql, val)

if __name__ == '__main__':
    pass
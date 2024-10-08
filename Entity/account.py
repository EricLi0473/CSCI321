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


    def get_premium_accountId(self) -> list:
        sql = "SELECT accountId FROM account WHERE profile = 'premium'"
        list = []
        for id in self.fetchAll(sql,""):
            list.append(id['accountId'])
        return list

    def verify_account_by_email(self, email):
        sql = "SELECT accountId FROM account WHERE email = %s"
        val = (email,)
        result = self.fetchOne(sql, val)
        if result:
            return True
        else:
            return False

    def get_account_by_accountId(self,accountId) -> dict:
        sql = "select * from account where accountId = %s"
        val = (accountId,)
        return self.fetchOne(sql,val)

    def get_all_account(self):
        sql = "select * from account WHERE profile != 'admin'"
        return self.fetchAll(sql,"")

    def get_accounts_by_userName(self, userName, accountId) -> list[dict]:
        if not userName:
            return []
        sql = "SELECT * FROM account WHERE userName LIKE %s AND accountId != %s AND profile != 'admin'"

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
                             investmentExperience, riskTolerance, investmentGoals, profile,isPrivateAccount,mlViewLeft,card_number,nextPaymentDate) -> bool:
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
            mlViewLeft = %s,
            card_number = %s,
            nextPaymentDate = %s
        WHERE accountId = %s
        """
        values = (
        userName, email, bio, age, sex, occupation, incomeLevel, netWorth, investmentExperience, riskTolerance,
        investmentGoals, profile, isPrivateAccount,mlViewLeft,card_number,nextPaymentDate,accountId)

        try:
            self.commit(sql, values)
            return True
        except Exception as e:
            print(f"Error updating personal info: {e}")
            return False

    def signUp(self, userName, hashedPassword, email, profile, age, sex, occupation, incomeLevel, netWorth,
               investmentExperience, riskTolerance, investmentGoals,apikey,card_number,nextPaymentDate) -> dict:

        sql = """
        INSERT INTO account 
        (userName, hashedPassword, email, profile, age, sex, occupation, incomeLevel, netWorth, investmentExperience, riskTolerance, investmentGoals,apikey,card_number,nextPaymentDate) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s,%s,%s,%s)
        """
        val = (userName, hashedPassword, email, profile, age, sex, occupation, incomeLevel, netWorth,
                        investmentExperience, riskTolerance, investmentGoals,apikey,card_number,nextPaymentDate)

        lastId = self.commit(sql, val)
        sql = 'SELECT * FROM account WHERE accountId = %s'
        val = (lastId,)
        return self.fetchOne(sql, val)
    def reset_pwd(self,email,hashedPassword):
        sql = "Update account set hashedPassword = %s WHERE email = %s"
        val = (hashedPassword, email)
        return self.commit(sql, val)

    def verify_AccountBy_apikey(self,key):
        sql = "SELECT * from account where apikey = %s And profile = 'premium'"
        val = (key,)
        return self.fetchOne(sql, val)

    def reset_mlView(self):
        sql = "UPDATE account SET mlViewLeft = 10"
        self.commit(sql,"")

    def detectDuplicateEmail(self,email):
        sql = '''SELECT
    CASE
        WHEN EXISTS (SELECT 1 FROM account WHERE email = %s)
        THEN TRUE
        ELSE FALSE
    END AS email_exists;
    '''
        return self.fetchOne(sql, (email,))['email_exists']

    def get_AllThresholds_by_account(self):
        sql = '''
        SELECT
    ts.accountId,
    ts.thresholdId,
    ts.stockSymbol,
    ts.changePercentage,
    a.email,
    p.receiveNotification
FROM
    thresholdSettings ts
LEFT JOIN
    account a ON ts.accountId = a.accountId
LEFT JOIN
    preferences p ON ts.accountId = p.accountId
WHERE
    a.profile = 'premium'
        '''
        return self.fetchAll(sql,"")
if __name__ == '__main__':
    print(Account().get_AllThresholds_by_account())
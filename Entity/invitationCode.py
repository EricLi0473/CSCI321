import mysql.connector
class InvitationCode:
    def __init__(self):
        self.mydb = self.connectToDatabase()
    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321"
        )
    def fetchOne(self,sql,val) -> tuple:
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchAll(self,sql,val) -> tuple:
        cursor = self.mydb.cursor(dictionary=True)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self,sql,val):
        cursor = self.mydb.cursor()
        cursor.execute(sql, val)
        self.mydb.commit()
    def verifyInvite_AND_Return_CompanyId(self,invitationCode) -> str or Exception:
        sql = 'SELECT * from invitationCode left join company on invitationCode.companyId = company.companyId where code=%s'
        result = self.fetchOne(sql,(invitationCode,))
        if not result:
            raise Exception('InvitationCode does not exist')
        self.decreaseCount(invitationCode)
        return result['companyId']
    def decreaseCount(self,invitationCode):
        try:
            sql = 'UPDATE invitationCode set count=count-1 where code=%s'
            self.commit(sql,(invitationCode,))
        except Exception as e:
            raise Exception("Your company's invitation codes have been used up")
    def insertInvitationCode(self,invitationCode,companyId,count = 10):
        sql = 'INSERT INTO invitationCode (code,conpanyId,count) VALUES (%s,%s)'
        val = (invitationCode,companyId,count)
        self.commit(sql,val)

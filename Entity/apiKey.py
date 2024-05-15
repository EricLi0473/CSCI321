import mysql.connector
class ApiKey:
    def __init__(self,keyHashedValue = None,keyCreateDate = None,keyStatus = 'valid', keyOwnerName = None, keyOwnerOccupation = None, keyUsageCount = None):
        self.keyHashedValue = keyHashedValue
        self.keyCreateDate = keyCreateDate
        self.keyStatus = keyStatus
        self.keyOwnerName = keyOwnerName
        self.keyOwnerOccupation = keyOwnerOccupation
        self.keyUsageCount = keyUsageCount

    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321"
        )
    def storeAnApiKey(self,keyHashedValue,keyOwnerName,keyOwnerOccupation) -> None:
        mydb = self.connectToDatabase()
        sql = "INSERT INTO apikeys (keyHashedValue, keyStatus, keyOwnerName, keyOwnerOccupation,keyUsageCount) VALUES (%s, %s, %s,%s,%s)"
        val = (keyHashedValue, "valid", keyOwnerName, keyOwnerOccupation,"0")
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def verifyAnApiKey(self, InputKeyHashedValue:str) -> bool:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM apikeys WHERE keyHashedValue = %s"
        cursor = mydb.cursor()
        cursor.execute(sql, (InputKeyHashedValue,))
        result = cursor.fetchall()
        cursor.close()
        return True if result else False

    def getAllApiKeysInfo(self) -> list:
        apikeyInfoList = []
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM apikeys"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for keyInfo in result:
            newApiKeyInfo = ApiKey(keyInfo[0], keyInfo[1], keyInfo[2], keyInfo[3], keyInfo[4], keyInfo[5])
            apikeyInfoList.append(newApiKeyInfo)
        cursor.close()
        return  apikeyInfoList

    def getApiKeysByHashedValue(self, keyHashedValue:str) -> list:
        mydb = self.connectToDatabase()
        sql = "SELECT * FROM apikeys WHERE keyHashedValue LIKE %s"
        cursor = mydb.cursor()
        cursor.execute(sql, ('%' + keyHashedValue + '%',))
        result = cursor.fetchall()
        apiKeyData = [ApiKey(*_) for _ in result]
        cursor.close()
        return apiKeyData

    def apiKeyUsageCountPlusOne(self,keyHashedValue:str) -> None:
        mydb = self.connectToDatabase()
        sql = 'UPDATE apikeys SET keyUsageCount = keyUsageCount + 1 WHERE keyHashedValue = %s'
        val = (keyHashedValue,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def freezeAnApiKey(self,keyHashedValue) -> None:
        mydb = self.connectToDatabase()
        sql = "UPDATE apikeys SET keyStatus = 'invalid' WHERE keyHashedValue = %s "
        val = (keyHashedValue,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def unFreezeAnApiKey(self,keyHashedValue) -> None:
        mydb = self.connectToDatabase()
        sql = "UPDATE apikeys SET keyStatus = 'valid' WHERE keyHashedValue = %s "
        val = (keyHashedValue,)
        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()

    def deleteApiKeyByHashedValue(self, keyHashedValue) -> bool and str:
        try:
            mydb = self.connectToDatabase()
            sql = "DELETE FROM apikeys WHERE keyHashedValue = %s"
            cursor = mydb.cursor()
            cursor.execute(sql, (keyHashedValue,))
            mydb.commit()
            cursor.close()
            mydb.close()
        except Exception:
            return False,'Can not delete this key, because the APIKey is bound to another account or has been used.'
        else:
            return True,'Deleted successfully.'

# apiKey().storeAnApiKey('1234567','valid','valid','valid')
# print(ApiKey().verifyAnApiKey("8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"))
# print(ApiKey().getAllApiKeysInfo()[0].keyHashValue)


from Entity.notification import Notification
class NotificationController:
    def __init__(self):
        pass

    def get_notifications_by_accountId(self,accountId):
        return Notification().get_notifications_by_accountId(accountId)

    def set_notification(self,accountId,notification,notificationType,referenceId,symbol):
        Notification().set_notification(accountId,notification,notificationType,referenceId,symbol)

    def delete_notification(self,notificationId):
        Notification().delete_notification(notificationId)

if __name__ == '__main__':
    import hashlib


    def string_to_int(s):
        hash_object = hashlib.md5(s.encode())
        hex_dig = hash_object.hexdigest()
        return int(hex_dig, 16) % (2 ** 31 - 1)


    # 示例字符串
    string = "bili"
    result = string_to_int(string)
    print(result)  # 输出一个小于 2^31-1 的整数
    # hashedSymbol = ''.join(str(ord(char)) for char in "1111")
    # NotificationController().set_notification(1,"welcome","threshold",hashedSymbol)
    # print(Notification().get_notifications_by_accountId("1"))
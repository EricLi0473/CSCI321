from Entity.notification import Notification
class NotificationController:
    def __init__(self):
        pass

    def get_notifications_by_accountId(self,accountId):
        return Notification().get_notifications_by_accountId(accountId)

if __name__ == '__main__':
    print(Notification().get_notifications_by_accountId("1"))
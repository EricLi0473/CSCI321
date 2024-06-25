from Entity.notification import Notification
class NotificationController:
    def __init__(self):
        pass

    def get_notifications_by_accountId(self,accountId):
        return Notification().get_notifications_by_accountId(accountId)

    def set_notification(self,accountId,notification,notificationType,referenceId):
        Notification().set_notification(accountId,notification,notificationType,referenceId)

if __name__ == '__main__':
    print(Notification().get_notifications_by_accountId("1"))
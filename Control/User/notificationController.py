from Entity.notification import Notification
class NotificationController:
    def __init__(self):
        pass

    def get_notifications_by_accountId(self,accountId):
        return Notification().get_notifications_by_accountId(accountId)

    def set_notification(self, accountId, notification, notificationType, referenceId, symbol):
        Notification().set_notification(accountId, notification, notificationType, referenceId, symbol)
        return True

    def delete_notification(self,notificationId):
        Notification().delete_notification(notificationId)

if __name__ == '__main__':
    print(NotificationController().set_notification("1",
                                                    "dsadssadsa",
                                                    "friend_threshold", "1991720094", "AAPL"))
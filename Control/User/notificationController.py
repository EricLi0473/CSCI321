from Entity.notification import Notification
class NotificationController:
    def __init__(self):
        pass

    def get_notifications_by_accountId(self,accountId):
        return Notification().get_notifications_by_accountId(accountId)

    def set_notification(self, accountId, notification, notificationType, referenceId, symbol):
        allNotifications = Notification().get_all_notifications()
        # transfer input to str, (database allow str input as numeric)
        accountId = str(accountId)
        notification = str(notification)
        notificationType = str(notificationType)
        referenceId = str(referenceId)
        symbol = str(symbol)
        # if database data: str == input:str, duplicate data , false to insert
        for notif in allNotifications:
            if (str(notif['accountId']) == accountId and
                    notif['notification'] == notification and
                    notif['notificationType'] == notificationType and
                    str(notif['referenceId']) == referenceId and
                    notif['symbol'] == symbol):
                return False
        # if !=, insert
        Notification().set_notification(accountId, notification, notificationType, referenceId, symbol)
        return True

    def delete_notification(self,notificationId):
        Notification().delete_notification(notificationId)

if __name__ == '__main__':
    print(NotificationController().set_notification("1",
                                                    "dsadssadsa",
                                                    "friend_threshold", "1991720094", "AAPL"))
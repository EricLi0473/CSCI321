from Entity.notification import *
class Remove_notification_by_id():
    def __init__(self):
        pass

    def remove_notification_by_id(self, notification_id):
        Notification().remove_notification_by_id(notification_id)
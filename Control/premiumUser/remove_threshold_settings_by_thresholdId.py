from Entity.thresholdSettings import *
class Remove_threshold_settings_by_thresholdId():
    def __init__(self):
        pass

    def remove_threshold_settings_by_thresholdId(self, thresholdId):
        ThresholdSettings().remove_threshold_settings_by_thresholdId(thresholdId)
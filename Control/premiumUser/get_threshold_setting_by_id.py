from Entity.thresholdSettings import *
class GetThresholdSettingById:
    def __init__(self):
        pass

    def get_threshold_settings_by_id(self, id):
        return ThresholdSettings().get_threshold_settings_by_id(id)

if __name__ == '__main__':
    print(GetThresholdSettingById().get_threshold_settings_by_id(1))
from Entity.thresholdSettings import *
class Update_threshold_settings():
    def __init__(self):
        pass

    # Automatically determines when a threshold is set, adds a threshold if one is not set, and updates it if one is available
    def update_threshold_settings(self, accountId, symbol: str, thresholdFigure: float):
        symbol = symbol.upper()
        if thresholdFigure == 0.0:
            ThresholdSettings().remove_threshold_settings_by_info(accountId,symbol)
            return True
        ThresholdSettings().insert_threshold_settings_by_id(accountId, symbol, thresholdFigure)
        return True
if __name__ == '__main__':
    Update_threshold_settings().update_threshold_settings("2","bili","0.121")
from Entity.thresholdSettings import *
class Get_threshold_by_symbol_and_id():
    def __init__(self):
        pass

    def get_threshold_by_symbol_and_id(self,accountId,symbol):
        thresholdList = ThresholdSettings().get_threshold_settings_by_id(accountId)
        for threshold in thresholdList:
            if symbol.upper() == threshold['stockSymbol'].upper():
                return threshold['changePercentage']
        return None

if __name__ == '__main__':
    print(Get_threshold_by_symbol_and_id().get_threshold_by_symbol_and_id('1','aapl'))

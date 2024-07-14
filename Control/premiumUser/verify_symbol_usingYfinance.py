import yfinance as yf
class verify_symbol_usingYfinance:
    def __init__(self):
        pass

    def verify_symbol_usingYfinance(self,symbol):
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        if hist.empty:
            raise Exception("No data found, symbol may be delisted")


if __name__ == '__main__':
    print(verify_symbol_usingYfinance().verify_symbol_usingYfinance('aapl'))

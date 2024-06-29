import yfinance as yf
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
class StockDataController:
    def __init__(self):
        pass

    def search_stock(self, content):
        api_key = '1TI3ZQ9MXCZ08O3M'
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={content}&apikey={api_key}"
        response = requests.get(url).json()
        best_matches = response.get("bestMatches", [])
        results = []

        def fetch_stock_data(stock):
            try:
                symbol = stock['1. symbol']

                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
                response = requests.get(url).json()
                global_quote = response.get('Global Quote', {})
                key_mapping = {
                    "absolute_change": "09. change",
                    "price": "05. price",
                    "relative_change": "10. change percent",
                    "symbol": "01. symbol",
                    "upsAndDowns": "09. change",
                    "volume": "06. volume"
                }

                if global_quote.get(key_mapping["volume"]) == "0":
                    return None

                new_data = {
                    "absolute_change": float(global_quote[key_mapping["absolute_change"]]),
                    "price": float(global_quote[key_mapping["price"]]),
                    "relative_change": float(global_quote[key_mapping["relative_change"]].replace('%', '')),
                    "symbol": global_quote[key_mapping["symbol"]],
                    "upsAndDowns": 1 if float(global_quote[key_mapping["upsAndDowns"]]) > 1 else 0,
                    "longName": stock['2. name'],
                    "volume": global_quote[key_mapping["volume"]]
                }

                # 修改符号，替换 .LON 为 .L
                if '.' in new_data['symbol']:
                    if '.LON' in new_data['symbol']:
                        new_data['symbol'] = new_data['symbol'].replace('.LON', '.L')
                    if '.DEX' in new_data['symbol']:
                        new_data['symbol'] = new_data['symbol'].replace('.DEX', '.DE')
                    if '.SAO' in new_data['symbol']:
                        new_data['symbol'] = new_data['symbol'].replace('.SAO', '.SA')
                    if '.SHH' in new_data['symbol']:
                        new_data['symbol'] = new_data['symbol'].replace('.SHH', '.SS')
                    if '.FRK' in new_data['symbol']:
                        new_data['symbol'] = new_data['symbol'].replace('.FRK', '.F')
                    if '.AMS' in new_data['symbol']:
                        new_data['symbol'] = new_data['symbol'].replace('.AMS', '.AS')

                return new_data
            except Exception as e:
                print(f"Error fetching data for {stock['1. symbol']}: {e}")
                return None

        # 使用并发来处理每个股票数据的获取
        with ThreadPoolExecutor() as executor:
            future_to_stock = {executor.submit(fetch_stock_data, stock): stock for stock in best_matches}

            for future in as_completed(future_to_stock):
                stock_data = future.result()
                if stock_data:
                    results.append(stock_data)

        return results


    def get_recommendation_stock_by_preference(self, countries='us',industries='Technology') -> list:
        url = f"https://api.marketaux.com/v1/entity/stats/intraday?interval=year&industries={industries}&countries={countries}&published_after=2024-01-01&api_token=ILqmhd82JOP8Feo9YFwxoFca82e8mzasKWG4jYKe"
        response = requests.get(url).json()
        recommendation_stock_list = []
        for stock in response['data'][0]['data']:
            recommendation_stock_list.append(stock['key'])

        return recommendation_stock_list
    def convert_market_cap(self,value):
        if value >= 1e12:
            return f"{value / 1e12:.2f}T"
        elif value >= 1e9:
            return f"{value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"{value / 1e6:.2f}M"
        elif value >= 1e3:
            return f"{value / 1e3:.2f}K"
        else:
            return str(value)
    def get_stock_info_minimum(self,symbol):
        df = yf.download(symbol, period="5d")
        df = df.reset_index()
        df["Close"] = round(df["Close"], 2)
        df["Open"] = round(df["Open"], 2)
        df["High"] = round(df["High"], 2)
        df["Low"] = round(df["Low"], 2)
        df['timestamp'] = df['Date'].apply(lambda x: int(x.timestamp() * 1000))  # 转换为Unix时间戳（毫秒）

        result = df[['timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']].rename(
            columns={
                'Open': 'open',
                'Close': 'close',
                'High': 'high',
                'Low': 'low',
                'Volume': 'volume'
            }
        ).to_dict(orient='records')

        data_dict = {}
        data_dict['absolute_change'] = round(result[-1]['close'] - result[-2]['close'], 2)
        data_dict["relative_change"] = round(((result[-1]['close'] - result[-2]['close']) / result[-2]['close'] * 100), 2)
        data_dict['upsAndDowns'] = 1 if data_dict['absolute_change'] >= 0 else 0
        data_dict['price'] = result[-1]['close']
        data_dict['symbol'] = symbol.upper()
        info = yf.Ticker(symbol).info
        data_dict['longName'] = info.get('longName', 'N/A')
        return data_dict
    def get_stock_info_medium(self,symbol):
        if isinstance(symbol, str):
            df = yf.download(symbol, period="30d")
            df = df.reset_index()
            df["Close"] = round(df["Close"], 2)
            df["Open"] = round(df["Open"], 2)
            df["High"] = round(df["High"], 2)
            df["Low"] = round(df["Low"], 2)
            df['timestamp'] = df['Date'].apply(lambda x: int(x.timestamp() * 1000))  # 转换为Unix时间戳（毫秒）

            result = df[['timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']].rename(
                columns={
                    'Open': 'open',
                    'Close': 'close',
                    'High': 'high',
                    'Low': 'low',
                    'Volume': 'volume'
                }
            ).to_dict(orient='records')

            data_dict = {}
            data_dict['absolute_change'] = round(result[-1]['close'] - result[-2]['close'], 2)
            data_dict["relative_change"] = round(((result[-1]['close'] - result[-2]['close']) / result[-2]['close'] * 100), 2)
            data_dict['upsAndDowns'] = 1 if data_dict['absolute_change'] >= 0 else 0
            data_dict['price'] = result[-1]['close']
            data_dict['symbol'] = symbol.upper()
            info = yf.Ticker(symbol).info
            data_dict['longName'] = info.get('longName', 'N/A')
            data_dict["data"] = result
            return data_dict
        else:
            symbol = [item.upper() for item in symbol]
            symbol_str = " ".join(symbol)
            tickers = yf.Tickers(symbol_str)
            result_list = []

            for ticker in tickers.tickers.keys():
                try:
                    df = tickers.tickers[ticker].history(period="5d").reset_index()
                    df["Close"] = round(df["Close"], 2)
                    df["Open"] = round(df["Open"], 2)
                    df["High"] = round(df["High"], 2)
                    df["Low"] = round(df["Low"], 2)
                    df['timestamp'] = df['Date'].apply(lambda x: int(x.timestamp() * 1000))  # 转换为Unix时间戳（毫秒）

                    result = df[['timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']].rename(
                        columns={
                            'Open': 'open',
                            'Close': 'close',
                            'High': 'high',
                            'Low': 'low',
                            'Volume': 'volume'
                        }
                    ).to_dict(orient='records')

                    data_dict = {}
                    data_dict['absolute_change'] = round(result[-1]['close'] - result[-2]['close'], 2)
                    data_dict["relative_change"] = round(
                        ((result[-1]['close'] - result[-2]['close']) / result[-2]['close'] * 100), 2)
                    data_dict['upsAndDowns'] = 1 if data_dict['absolute_change'] >= 0 else 0
                    data_dict['price'] = result[-1]['close']
                    data_dict['symbol'] = ticker  # 使用 ticker 而不是 symbol.upper()，以确保正确的股票符号
                    info = tickers.tickers[ticker].info
                    data_dict['longName'] = info.get('longName', 'N/A')
                    data_dict["data"] = result

                    result_list.append(data_dict)
                except Exception:
                    continue
            return result_list
    def get_update_stock_data(self,symbol, period):
        df = yf.download(symbol, period=period)
        df = df.reset_index()
        df["Close"] = round(df["Close"], 2)
        df["Open"] = round(df["Open"], 2)
        df["High"] = round(df["High"], 2)
        df["Low"] = round(df["Low"], 2)
        df['timestamp'] = df['Date'].apply(lambda x: int(x.timestamp() * 1000))  # 转换为Unix时间戳（毫秒）

        result = df[['timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']].rename(
            columns={
                'Open': 'open',
                'Close': 'close',
                'High': 'high',
                'Low': 'low',
                'Volume': 'volume'
            }
        ).to_dict(orient='records')
        return result

    def get_stock_info_full(self,symbol):
        data_dict = {}
        df = yf.download(symbol, period="5d")
        df = df.reset_index()
        df["Close"] = round(df["Close"], 2)
        df["Open"] = round(df["Open"], 2)
        df["High"] = round(df["High"], 2)
        df["Low"] = round(df["Low"], 2)
        data_dict["closeDate"] = df.iloc[-1]['Date'].strftime('%b %d')
        df['timestamp'] = df['Date'].apply(lambda x: int(x.timestamp() * 1000))  # 转换为Unix时间戳（毫秒）

        result = df[['timestamp', 'Open', 'Close', 'High', 'Low', 'Volume']].rename(
            columns={
                'Open': 'open',
                'Close': 'close',
                'High': 'high',
                'Low': 'low',
                'Volume': 'volume'
            }
        ).to_dict(orient='records')

        data_dict['absolute_change'] = round(result[-1]['close'] - result[-2]['close'], 2)
        data_dict["relative_change"] = round(((result[-1]['close'] - result[-2]['close']) / result[-2]['close'] * 100), 2)
        data_dict['upsAndDowns'] = 1 if data_dict['absolute_change'] >= 0 else 0
        data_dict['price'] = result[-1]['close']

        info = yf.Ticker(symbol).info
        data_dict['symbol'] = info.get('symbol', symbol)
        data_dict['longName'] = info.get('longName', 'N/A')
        data_dict['currency'] = info.get('currency', 'USD')
        # data_dict["data"] = result
        data_dict["marketCap"] = self.convert_market_cap(info.get('marketCap', 0))
        data_dict["trailingPE"] = round(info.get('trailingPE',0),2)
        company = {}
        company['longBusinessSummary'] = info.get('longBusinessSummary', 'N/A')
        company['fullTimeEmployees'] = info.get('fullTimeEmployees', 'N/A')
        company['address1'] = info.get('address1', 'N/A')
        company['city'] = info.get('city', 'N/A')
        company['zip'] = info.get('zip', 'N/A')
        company['country'] = info.get('country', 'N/A')
        company['phone'] = info.get('phone', 'N/A')
        company['website'] = info.get('website', 'N/A')
        company['longName'] = info.get('longName', 'N/A')
        company['industry'] = info.get('industry', 'N/A')
        company['sector'] = info.get('sector', 'N/A')
        company['exchange'] = info.get('exchange', 'N/A')
        data_dict['company'] = company
        return data_dict

if __name__ == '__main__':
    alist = ['NVDA', 'AAPL', 'MSFT', 'SONY', 'AMD', 'AVGO', 'AVGOP', 'SMCI', 'INTC', 'CSCO', 'ORCL', 'MU', 'IBM', 'SAP', 'SAPGF', '4333.HK', 'PLTR', 'AMAT', 'SNOW', 'UBER']
    # print(StockDataController().get_stock_info_medium(list))
    print(StockDataController().get_update_stock_data("NVDA","1mo"))



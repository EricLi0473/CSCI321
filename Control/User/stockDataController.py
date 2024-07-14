import yfinance as yf
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import random
from cachetools import LRUCache,cached
import time
class StockDataController:
    _instance = None
    cache = LRUCache(maxsize=128)
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StockDataController, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        pass
    @cached(cache=cache)
    def get_common_symbol_data(self):
        url = f"https://api.marketaux.com/v1/entity/stats/aggregation?api_token=ILqmhd82JOP8Feo9YFwxoFca82e8mzasKWG4jYKe&countries=us"
        response = requests.get(url)
        list = []
        count = 0
        for symbol in response.json().get('data'):
            try:
                count +=1
                if count > 10:
                    break
                list.append(self.get_stock_info_medium(symbol['key']))
            except Exception:
                continue
        return list
    def fetch_stock_data(self,country:str, industry:str):
        API_TOKEN = "ILqmhd82JOP8Feo9YFwxoFca82e8mzasKWG4jYKe"
        url = f"https://api.marketaux.com/v1/entity/stats/aggregation?countries={country}&industries={industry}&api_token={API_TOKEN}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            return []
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

                # 定义符号映射字典
                symbol_mapping = {
                    '.LON': '.L',
                    '.DEX': '.DE',
                    '.SAO': '.SA',
                    '.SHH': '.SS',
                    '.FRK': '.F',
                    '.AMS': '.AS',
                    '.BSE': '.BO'
                }

                # 替换符号
                if '.' in new_data['symbol']:
                    for old_suffix, new_suffix in symbol_mapping.items():
                        if old_suffix in new_data['symbol']:
                            new_data['symbol'] = new_data['symbol'].replace(old_suffix, new_suffix)

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

    def get_recommendation_stock_by_preference(self, countries:list,industries:list) -> list:
        stock_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for country in countries:
                for industry in industries:
                    futures.append(executor.submit(self.fetch_stock_data, country, industry))

            for future in concurrent.futures.as_completed(futures):
                stock_data.extend(future.result())

        # Get unique stock symbols
        stock_symbols = list(set([item['key'] for item in stock_data]))

        # Ensure we have at least 20 symbols, repeating if necessary
        while len(stock_symbols) < 20:
            stock_symbols.extend(stock_symbols[:20 - len(stock_symbols)])

        return random.sample(stock_symbols, 20)

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
            df = yf.download(symbol, period="1mo")
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

    def get_update_stock_data(self, symbol, period):

        retries = 3
        for i in range(retries):
            try:
                df = yf.download(symbol, period=period)
                break
            except Exception as e:
                if i == retries - 1:
                    return {"error": f"Failed to download data for {symbol} after {retries} retries: {e}"}
                time.sleep(2 ** i)  # The indexes are retreating for a retest.

        if df.empty:
            return {"error": f"No data found for {symbol}"}

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

    def get_stock_info_full(self, symbol):

        data_dict = {}

        retries = 3
        for i in range(retries):
            try:
                df = yf.download(symbol, period="5d")
                break
            except Exception as e:
                if i == retries - 1:
                    return {"error": f"Failed to download data for {symbol} after {retries} retries: {e}"}
                time.sleep(2 ** i)  # 指数退避重试

        if df.empty:
            return {"error": f"No data found for {symbol}"}

        df = df.reset_index()
        df["Close"] = round(df["Close"], 2)
        df["Open"] = round(df["Open"], 2)
        df["High"] = round(df["High"], 2)
        df["Low"] = round(df["Low"], 2)

        try:
            data_dict["closeDate"] = df.iloc[-1]['Date'].strftime('%b %d')
        except Exception as e:
            return {"error": f"Failed to process date for {symbol}: {e}"}

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

        if len(result) < 2:
            return {"error": f"Not enough data to calculate changes for {symbol}"}

        data_dict['absolute_change'] = round(result[-1]['close'] - result[-2]['close'], 2)
        data_dict["relative_change"] = round(((result[-1]['close'] - result[-2]['close']) / result[-2]['close'] * 100),
                                             2)
        data_dict['upsAndDowns'] = 1 if data_dict['absolute_change'] >= 0 else 0
        data_dict['price'] = result[-1]['close']

        retries = 3
        for i in range(retries):
            try:
                info = yf.Ticker(symbol).info
                break
            except Exception as e:
                if i == retries - 1:
                    return {"error": f"Failed to fetch ticker info for {symbol} after {retries} retries: {e}"}
                time.sleep(2 ** i)  # 指数退避重试

        data_dict['symbol'] = info.get('symbol', symbol)
        data_dict['longName'] = info.get('longName', 'N/A')
        data_dict['currency'] = info.get('currency', 'USD')
        data_dict["marketCap"] = self.convert_market_cap(info.get('marketCap', 0))
        data_dict["trailingPE"] = round(info.get('trailingPE', 0), 2)

        company = {
            'longBusinessSummary': info.get('longBusinessSummary', 'N/A'),
            'fullTimeEmployees': info.get('fullTimeEmployees', 'N/A'),
            'address1': info.get('address1', 'N/A'),
            'city': info.get('city', 'N/A'),
            'zip': info.get('zip', 'N/A'),
            'country': info.get('country', 'N/A'),
            'phone': info.get('phone', 'N/A'),
            'website': info.get('website', 'N/A'),
            'longName': info.get('longName', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'exchange': info.get('exchange', 'N/A')
        }

        data_dict['company'] = company

        return data_dict

if __name__ == '__main__':
    print(StockDataController().get_common_symbol_data())



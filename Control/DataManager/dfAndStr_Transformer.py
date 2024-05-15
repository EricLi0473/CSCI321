from io import StringIO
import pandas as pd
class dfAndStr_Transformer():
    def __init__(self):
        pass
    @staticmethod
    def get_stock_data(symbol):
        try:
            import yfinance as yf
            from datetime import datetime, timedelta
            end_date = datetime.today().date()
            start_date = (end_date - timedelta(days=365 * 50))
            df = yf.download(symbol, start=start_date, end=end_date)
            all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
            df = df.reindex(all_dates)
            df = df.fillna(method='ffill')
        except Exception:
            raise Exception(f"Stock with symbol '{symbol}' not found.")
        return df
    def transferDFtoStr(self,df) -> str:
        return df.to_csv()

    def transferStrtoDF(self,dfStr) -> pd.DataFrame:
        newDf = pd.read_csv(StringIO(dfStr))
        if 'Date' in newDf.columns:
            newDf["Date"] = pd.to_datetime(newDf["Date"])
        elif 'Unnamed: 0' in newDf.columns:
            newDf["Date"] = pd.to_datetime(newDf["Unnamed: 0"])
        newDf.set_index("Date", inplace=True)
        newDf.drop(columns=['Unnamed: 0'], inplace=True)
        return newDf

# df = pd.read_csv("D:/Users/cesir/PycharmProjects/flaskProject/bili.csv")
# dfAndStr_Transformer = dfAndStr_Transformer()
# str = dfAndStr_Transformer.transferDFtoStr(df)

# print(dfAndStr_Transformer.transferStrtoDF(str).info())
#
# df = dfAndStr_Transformer.get_stock_data('aapl')
#
# str1 = dfAndStr_Transformer().transferDFtoStr(df)
# print(dfAndStr_Transformer().transferStrtoDF(str1).info())

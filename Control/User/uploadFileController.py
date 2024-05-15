import pandas
import pandas as pd
class UploadFileController:
    def __init__(self):
        pass

    '''''
    File upload
    tickerSymbol: must be the file title name
    column: [Date:yyyy-mm-dd:From history to the present, Open, High, Low, Close, Adj Close, Volume]
    The order can be switched
    '''''

    def checkUploadDataFormat(self,df:pd.DataFrame) -> bool and str:
        try:
            expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            if df.empty:
                return False, "DataFrame is empty"

            if not set(expected_columns).issubset(set(df.columns)):
                return False, f"DataFrame does not contain all expected columns {expected_columns}"

            if 'Date' in df.columns:
                try:
                    pd.to_datetime(df['Date'], format='%Y-%m-%d')
                except ValueError:
                    return False, "Date column is not in the format 'yyyy-mm-dd'"

            return True, "DataFrame format is correct"
        except Exception:
            return False, "You are not uploading a CSV format file."


# df = pd.read_csv('D:/Users/cesir/PycharmProjects/flaskProject/bili.csv')
# df["Date"] = pd.to_datetime(df["Date"])
# df.set_index("Date", inplace=True)
# file_name = getFileName('D:/Users/cesir/PycharmProjects/flaskProject/bili.csv')
# print(file_name)
# print(df.info())
    #
    # is_valid, message = checkUploadDataFormat(df)
    #
    # if is_valid:
    #     print(message)
    # else:
    #     print(message)






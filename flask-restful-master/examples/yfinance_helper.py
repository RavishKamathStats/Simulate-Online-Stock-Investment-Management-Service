import yfinance as yf
import pandas

def get_info(instrument):
    #data = yf.Ticker(instrument).history(period="1d", interval="1m")
    #return data["Close"].iloc[-1]
    ticker = yf.Ticker(instrument)
    df = ticker.history(period="1d")
    print('df: ', df)
    #print('df type: ', type(df))
    print('df keys: ', df.keys())
    #print('df index: ', df.index)
    #print('type of info: ', df.values.tolist())
    open_price = df["Open"][0]
    high_price = df["High"][0]
    low_price = df["Low"][0]
    close_price = df["Close"][0]
    volume = df["Volume"][0]
    dividends = df["Dividends"][0]
    stock_splits = df["Stock Splits"][0]

    print('high price: ', high_price)

    info_dict = [open_price, high_price, low_price, close_price]

    return info_dict
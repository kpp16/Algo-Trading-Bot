import yfinance as yf
import matplotlib.pyplot as plt

def collectData(ticker, startDate, endDate, period):
    tickerSymbol = ticker
    tickerData = yf.Ticker(tickerSymbol)

    tickerDF = tickerData.history(period=period, start=startDate, end=endDate)

    return tickerDF


def main():
    ticker = "RELIANCE.NS"
    startDate = "2021-05-26"
    endDate = "2021-06-26"
    period="1d"

    relData = collectData(ticker, startDate, endDate, period)
    closes = list(relData['Close'])
    # print(closes)
    time_period = [x for x in range(1, 24)]
    
    plt.plot(time_period, closes)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()


main()

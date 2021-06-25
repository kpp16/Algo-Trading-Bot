import yfinance as yf

def collectData(ticker, startDate, endDate, period):
    tickerSymbol = ticker
    tickerData = yf.Ticker(tickerSymbol)

    tickerDF = tickerData.history(period=period, start=startDate, end=endDate)

    return tickerDF


def main():
    ticker = "RELIANCE.NS"
    startDate = "2012-01-01"
    endDate = "2021-06-25"
    period="1d"

    relData = collectData(ticker, startDate, endDate, period)

    print("Open", "High", "Low")
    for i in range(-1, -11, -1):
        print(relData[len(relData) - i]['Open'], relData[len(relData) - i]['High'], relData[len(relData) - i]['Low'])

main()

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

clearance = 15

def collectData(ticker, startDate, endDate, period):
    tickerSymbol = ticker
    tickerData = yf.Ticker(tickerSymbol)

    tickerDF = tickerData.history(period=period, start=startDate, end=endDate)

    return tickerDF

def find_local_maxima(closes):
    local_maxima = {}
    for i in range(1, len(closes) - 1):
        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:
            local_maxima[i] = closes[i] + clearance
    
    return local_maxima

def find_local_minima(closes):
    local_minima = {}
    for i in range(1, len(closes) - 1):
        if closes[i] < closes[i - 1] and closes[i] < closes[i + 1]:
            local_minima[i] = closes[i] - clearance
    
    return local_minima

def main():
    ticker = "RELIANCE.NS"
    startDate = "2021-04-26"
    endDate = "2021-06-26"
    period="1d"

    relData = collectData(ticker, startDate, endDate, period)
    closes = list(relData['Close'])

    time_period = np.array([x for x in range(1, 45)])

    maximas = find_local_maxima(closes)
    minimas = find_local_minima(closes)

    maxima_closes = np.array(list(maximas.values()))
    maxima_time = np.array(list(maximas.keys()))

    minima_closes = np.array(list(minimas.values()))
    minima_time = np.array(list(minimas.keys()))

    fig = plt.figure()

    fig.add_subplot(231)
    plt.plot(maxima_time, maxima_closes, color='red')
    plt.plot(minima_time, minima_closes, color='green')
    plt.plot(time_period, closes)
    plt.xlabel("Time (Days since 2021-04-26)")
    plt.ylabel("Price (INR)")
    plt.title("RELIND.NS")

    red_patch = mpatches.Patch(color='red', label='Resistance')
    green_patch = mpatches.Patch(color='green', label='Securities')
    blue_patch = mpatches.Patch(color='blue', label='Close values')

    plt.legend(handles=[red_patch, green_patch, blue_patch])

    fig.add_subplot(232)
    plt.title("Maxima closes")
    plt.scatter(maxima_time, maxima_closes, color='red')
    red_patch112 = mpatches.Patch(color='red', label='Resistance')
    plt.xlabel("Time (Days since 2021-04-26)")
    plt.ylabel("Price (INR)")    
    plt.legend(handles=[red_patch112])

    fig.add_subplot(233)
    plt.title("Minima closes")
    plt.scatter(minima_time, minima_closes, color='green')
    green_patch113 = mpatches.Patch(color='green', label='Resistance')
    plt.xlabel("Time (Days since 2021-04-26)")
    plt.ylabel("Price (INR)")    
    plt.legend(handles=[green_patch113])


    plt.show()


main()

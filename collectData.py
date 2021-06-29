import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import linearRegression

threshold = 20

def collectData(ticker, startDate, endDate, period):
    tickerSymbol = ticker
    tickerData = yf.Ticker(tickerSymbol)

    tickerDF = tickerData.history(period=period, start=startDate, end=endDate)

    return tickerDF

def find_maxima(closes):
    maxima = {}
    for i in range(1, len(closes) - 1):
        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:
            maxima[i] = closes[i] + threshold
    
    return maxima

def find_minima(closes):
    minima = {}
    for i in range(1, len(closes) - 1):
        if closes[i] < closes[i - 1] and closes[i] < closes[i + 1]:
            minima[i] = closes[i] - threshold
    
    return minima

def find_minima_maxima_new(slope, intercept, n):
    # y = mx + c
    y = []

    for i in range(n):
        y.append((slope * i) + intercept)
    
    return y

def find_mid(maxima, minima, n):
    y = []
    for i in range(n):
        y.append((minima[i] + maxima[i]) / 2)
    
    return y

def get_breakout(ticker, startDate, endDate):
    # ticker = "ASIANPAINT.NS"
    # startDate = "2021-04-27"
    # endDate = "2021-06-27"
    period="1d"
    data = collectData(ticker, startDate, endDate, period)
    closes = list(data['Close'])
    time_period = [x for x in range(1, len(closes) + 1)]

    maxima_closes = np.array(list(find_maxima(closes).values()))
    maxima_time = np.array(list(find_maxima(closes).keys()))

    minima_closes = np.array(list(find_minima(closes).values()))
    minima_time = np.array(list(find_minima(closes).keys()))

    # print("Maxima:")
    max_int, max_slope = linearRegression.find_slope_intercept(maxima_time, maxima_closes)

    # print()

    # print("Minima:")
    min_int, min_slope = linearRegression.find_slope_intercept(minima_time, minima_closes)

    new_minima = find_minima_maxima_new(min_slope, min_int, len(time_period))
    new_maxima = find_minima_maxima_new(max_slope, max_int, len(time_period))
    mid = find_mid(new_maxima, new_minima, len(time_period))

    # print()
    # print("Today's Resistance:", new_maxima[-1])
    # print("Today's Security:", new_minima[-1])
    # print("Today's breakout:", mid[-1])

    # fig = plt.figure()

    # fig.add_subplot(221)
    # plt.title("ASIANPAINT.NS")
    # plt.plot(maxima_time, maxima_closes, color='green', label="Resistance")
    # plt.plot(minima_time, minima_closes, color='red', label="Security")
    # plt.plot(time_period, closes, color="blue", label="Close")
    # plt.legend()
    # plt.xlabel("Time")
    # plt.ylabel("Price")

    # fig.add_subplot(222)
    # plt.title("Resistance")
    # plt.scatter(maxima_time, maxima_closes, color='green', label="Resistance")
    # plt.plot(time_period, new_maxima, color="black")
    # plt.legend()
    # plt.xlabel("Time")
    # plt.ylabel("Price")

    # fig.add_subplot(223)
    # plt.title("Security")
    # plt.scatter(minima_time, minima_closes, color='red', label="Security")
    # plt.plot(time_period, new_minima, color="black")
    # plt.legend()
    # plt.xlabel("Time")
    # plt.ylabel("Price")

    # fig.add_subplot(224)
    # plt.title("ASIANPAINT.NS NEW")
    # plt.plot(time_period, new_maxima, color='green', label="Resistance")
    # plt.plot(time_period, new_minima, color='red', label="Security")
    # plt.plot(time_period, closes, color="blue", label="Close")
    # plt.plot(time_period, mid, color="purple", label="Mid")
    # plt.legend()
    # plt.xlabel("Time")
    # plt.ylabel("Price")

    # plt.show()

    return float(mid[-1][0])

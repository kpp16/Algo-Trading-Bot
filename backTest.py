from collectData import get_breakout, collectData
import datetime
import pandas as pd
import matplotlib.pyplot as plt

start_date_O = "2019-06-28"
end_date = "2020-01-28"
ticker = "SBIN.NS"

breakout = get_breakout(ticker, start_date_O, end_date)

print(breakout)

start_money = 10000
curr_money = 10000
holding = 0

start_date = "2020-01-29"
end_date = "2021-06-28"
newData = collectData(ticker, start_date, end_date, "1d")

closes = list(newData['Close'])

delta = [0]
final_val = 0

buy_count, sell_count = 0, 0

sold = True

for val in closes:
    if val < breakout:
        if holding > 0:
            sold = True
            print("Sell", val)
            curr_money += val
            holding -= 1
            sell_count += 1

    elif val > breakout and curr_money >= val:
            print("Buy", val)
            holding += 1
            curr_money -= val
            buy_count += 1
    
    delta.append(curr_money)

    date1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date1 + datetime.timedelta(days=1)
    end_date = end_date.strftime("%Y-%m-%d")
    breakout = get_breakout(ticker, start_date_O, end_date)
    # print("Breakout:", breakout)
    start_date = str(end_date)
    final_val = int(val)

time = [x for x in range(len(delta))]

print("Buy count:", buy_count)
print("Sell count:", sell_count)

print("First day buy, sell: ", (10000 - closes[0] + closes[-1]))

plt.plot(time, delta)
plt.show()

final_money = curr_money + holding*final_val

print()
print("Final Money: ", curr_money)
print("Holding:", holding)
print("Total Money:", final_money)
print("percentage increase:", ((final_money - start_money) / start_money)* 100)
print("CAGR:", ((final_money / 10000) ** (1 / 1.5)) - 1)
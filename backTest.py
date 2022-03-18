from collectData import get_breakout, collectData
import datetime
import csv

ticker = "TSLA"
filename = ticker + ".csv"

def write_into_csv(line):
    with open(filename, "a+") as f:
        writer = csv.writer(f)
        writer.writerow(line)

def back_test():
    with open(filename, "a+") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Buy/Sell", "Quantity", "Stock Price", "Amount (INR)", "Holding", "Total Money With Holds (INR)"])

    start_date_O = "2015-06-28"
    end_date = "2020-01-11"
    breakout = get_breakout(ticker, start_date_O, end_date)

    print(breakout)

    start_money = 10000
    curr_money = 10000
    holding = 0

    start_date = "2020-01-12"
    end_date = "2022-03-12"
    newData = collectData(ticker, start_date, end_date, "1d")

    closes = list(newData['Close'])

    delta = [0]
    final_val = 0

    buy_count, sell_count = 0, 0

    for val in closes:
        if val < breakout:
            if holding > 0:
                curr_money += val
                holding -= 1
                sell_count += 1
                print("Sell", 1, ticker, val, curr_money, holding)
                write_into_csv([ticker, "Sell", 1, val, curr_money, holding, curr_money + holding*val])          

        elif val > breakout and curr_money >= val:
                holding += 1
                curr_money -= val
                buy_count += 1
                print("Buy", 1, ticker, val, curr_money, holding)
                write_into_csv([ticker, "Buy", 1, val, curr_money, holding, curr_money + holding*val])
        else:
             write_into_csv([ticker, "None", 0, val, curr_money, holding, curr_money + holding*val])
        
        delta.append(curr_money)

        date1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = date1 + datetime.timedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d")
        breakout = get_breakout(ticker, start_date_O, end_date)
        # print("Breakout:", breakout)
        start_date = str(end_date)
        final_val = float(val)

    print("Buy count:", buy_count)
    print("Sell count:", sell_count)

    print("First day buy, sell: ", (10000 - closes[0] + closes[-1]))

    final_money = curr_money + holding*final_val

    print()
    print("Final val:", final_val)
    print("Final Money: ", curr_money)
    print("Holding:", holding)
    print("Total Money:", final_money)
    print("percentage increase:", ((final_money - start_money) / start_money)* 100)
    print("CAGR:", (((final_money / 10000) ** (1 / 1.5)) - 1) * 100, "%")

back_test()
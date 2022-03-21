import datetime

from collectData import get_breakout, collectData

import alpaca_trade_api as tradeapi
import time
import os
import websocket
import json

socket = "wss://stream.data.alpaca.markets/v2/iex"
api = tradeapi.REST()

API_KEY = os.getenv('APCA_API_KEY_ID')
SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')

start_date_O = "2015-06-28"
end_date = datetime.datetime.today().strftime('%Y-%m-%d')
ticker = "TSLA"
breakout = get_breakout(ticker, start_date_O, end_date)

account = api.get_account()

def timeMarketClose():
	clock = api.get_clock()
	return (clock.next_close - clock.timestamp).total_seconds()


def awaitMarketOpen():
    print("Market opening... Selling all the open positions")

    positions = api.list_positions() 
    for position in positions:
        quote = position.symbol
        qty = position.qty
        print(f"Selling {qty} {quote}")
        api.submit_order(
            symbol=quote,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )   

    clock = api.get_clock()
    if not clock.is_open:
        time_to_open = (clock.next_open - clock.timestamp).total_seconds()
        print("Waiting for the market to open...")
        time.sleep(round(time_to_open))


def on_open(ws):
    print("Opened websocket")

    auth_data = {
        "action": "auth",
        "key": API_KEY,
        "secret": SECRET_KEY
    }

    ws.send(json.dumps(auth_data))

    ticker_data = {"action":"subscribe", "bars":["AAPL"]}

    ws.send(json.dumps(ticker_data))


def on_message(ws, message):
    print("Message recieved: ", message) # Check for the dataype of message python

    json_acceptable_string = message.replace("'", "\"")
    message_d = json.loads(json_acceptable_string)

    req_keys = sorted(["T", "S", "o", "h", "l", "c", "v", "t"])
    given_keys = sorted(list(message_d.keys()))

    if req_keys == given_keys:
        set_order(message_d)


def on_close(ws):
    print("Closed connection")


def set_order(data):
    price = data["c"]
    found = False
    positions = api.list_positions() 

    for position in positions:
        if position.symbol == ticker:
            found = True
            break
    
    if price >= breakout and account.buying_power > price + 100: # check the buying power as well
        # buy
        api.submit_order(
            symbol=ticker,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    
        print("Buy", ticker, price)
    
    elif (price < breakout) and found:
        # sell
        api.submit_order(
            symbol=ticker,
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

        print("Buy", ticker, price)


def run():
    
    while (True):
        awaitMarketOpen()
        
        if timeMarketClose() <= 15*60:
            print("Market closing in 15 minutes... Closing all positions")

            positions = api.list_positions()
            for position in positions:
                quote = position.symbol
                qty = position.qty
                print(f"Selling {qty} {quote}")
                api.submit_order(
                    symbol=quote,
                    qty=qty,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
            print("Closing for the day")
            exit()

        ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)


if __name__ == "__main__":
    print("Bot started")
    run()

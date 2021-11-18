import json, config
from flask import Flask, request, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)


# Connect to Binance Exchange
client = Client(config.API_KEY, config.API_SECRET, tld='us')

# Connect to account
account = client.get_account()

# Create buy sell orders
def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

# Get USD balance and return 5% of total balance
def get_usd_balance(account):
    
    USD = [coin for coin in account['balances'] if coin['asset'] == 'USD']
    print(USD)
    return float(USD[0]['free']) *.05

# Home Page
@app.route("/")
def welcome():
    return render_template('index.html')

# Main Function
@app.route("/webhook", methods=['POST'])
def webhook():
    
    data = json.loads(request.data)
    
    side = data['strategy']['order_action'].upper()
    
    quantity = data['strategy']['order_contracts']
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return{
            "code": "error",
            "message": "Nice try, invalid passphrase"
        } 
    
    trade_amout = get_usd_balance(account)
    
    order_responce = order(side, trade_amount , data['ticker'])
    
    if order_responce:
        return {
            "code":"success"
        }
    else:
        print("order failed")
        
        return{
            "code":"error",
            "message": "order failed"
        }
    
    print(order_responce)
    
    return data
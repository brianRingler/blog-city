from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint


symbols = 'ETH,BTC,ADA,DOT,UNI,LTC,LINK,VET,MINA,SWAP,RFOX,ATOM,CRV,MATIC,GUSD'
symbol_list = ['ETH','BTC','ADA','DOT','UNI','LTC','LINK','VET','MINA','SWAP','RFOX','ATOM','CRV','MATIC','GUSD']

def current_market_prices(symbols, symbol_list):
    market_prices = {}
    api_key = 'f90cdedd-0ca6-4c44-85e8-98124f304753'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    parameters = {
    'symbol': symbols
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters, headers=headers)
        data = json.loads(response.text)
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        
    for symbol in symbol_list:
        price = round(data.get('data', {}).get(symbol, {}).get('quote', {}).get('USD', {}).get('price', {}),2)
        market_prices[symbol] = price
    return market_prices



# pprint.pprint(current_market_prices(symbols, symbol_list))
        
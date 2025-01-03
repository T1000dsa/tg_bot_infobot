import requests
base_url = 'http://api.coinlayer.com/live'
symbols = 'BTC,ETH,SOL,USDT,XRP,SUI,TON,ADA,BNB,AVAX'
put_it = {'access_key':'dff048a35cc8bef2d84b9d57951ab629', 'symbols':symbols}
def do_request_cry() -> dict:
    try:
        respone = requests.get(base_url, params=put_it)
    except:
        print('Some failure here')
    return respone.json()
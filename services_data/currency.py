import requests
base_url = 'https://api.currencylayer.com/live'
value = 'EUR,GBP,RUB,JPY,CNY,TRY'
put_it = {'access_key':'a9c806aaf6102eaa617c91b516690ead', 'currencies':value}
def do_request() -> dict:
    try:
        respone = requests.get(base_url, params=put_it)
    except:
        print('Some failure here')
    return respone.json()
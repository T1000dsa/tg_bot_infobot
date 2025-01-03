import requests
class Quotes:
    '''
    Choice mode 0 if you want to get a intraday statistic, choice mode 1 if you want to get a monthly statistic
    '''
    def __init__(self, mode='0'):
        self.__key = 'TX8Z2B5NDRJ8709W'
        self.__ist = ['NDAQ', 'IBM', 'BA', 
                      'GM', 'CVX', 'BAC', 
                      'INTC', 'MSFT', 'GOOGL',
                      'EBAY', 'NVDA', 'JPM', 
                      'KO'] # List of tickets american companies
        if mode == '0':
            self.__url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey={}'
        if mode == '1':
            self.__url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={}&apikey={}'
        
    def show_it(self, company) -> tuple[str, dict]:
        try:
            responce = requests.get(self.__url.format(company, self.__key))
            return (company, responce.json()['Time Series (5min)'])
        except(Exception) as err: 
            raise err
    @property
    def give_main(self):
        try:
            for i in self.__ist:
                responce = requests.get(self.__url.format(i, self.__key))
                yield (i, responce.json())
        except(Exception) as err: 
            raise err
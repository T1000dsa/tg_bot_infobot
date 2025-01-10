import requests
from bs4 import BeautifulSoup
import os
from lexicon_data.lexicon import LEXICON
class Eco_data:
    def __init__(self):
        self.__result = []
        self.__url = 'https://ru.wikipedia.org/wiki/Список_стран_по_ВВП_(номинал)'  # Замените на нужный URL
        self.__data = {'user-agent':'Yandex'}
    # Отправляем GET-запрос

    def give_data(self) -> str:
        try:
            with open(f'{os.getcwd()}/services_data/result.html', encoding='utf-8') as filex:
                soup = BeautifulSoup(filex, 'html.parser')

        

        except(Exception) as err:
            print('Some failure here', err)
            response = requests.get(self.__url, headers=self.__data)
            with open(f'{os.getcwd()}/services_data/result.html', 'w', encoding='utf-8') as filexy:
                filexy.write(response.text)

        finally:
            with open(f'{os.getcwd()}/services_data/result.html', encoding='utf-8') as filex:
                soup = BeautifulSoup(filex, 'html.parser')

        for i in soup.find_all('table'):
            res = i.find('table', attrs={'class':'wikitable'})
            if res:
                for x in res:
                    for y in x.text.split():
                        self.__result.append(y)
        ist = []
        new = []
        c = 1
        for i in self.__result[6:]:
            ist.append(i)
            if c==3:
                c=0
                new.append(ist[1:])
                ist = []
            c+=1
        new = '\n'.join([f"{i[0]}: {i[1]}{LEXICON['doll']} {LEXICON['trill']}" for i in new[:12]])
        return new
            
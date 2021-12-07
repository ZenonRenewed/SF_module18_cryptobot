import requests
import json
from extensions import keys


class APIException(Exception): #защита остановки программы вследствии ошибки
    pass


class CryptoConverter: #конвертер валют
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base: #исключение приема двух одинаковых валют
            raise APIException(f'Невозможно перевести одинаковые валюты ({base})')

        try: #исключение приема несуществующией валюты, которую конвертируют
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try: #исключение приема несуществующей валюты, В которую конвертируют
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try: #исклчючение приема НЕ численных значений суммы
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}') #парсер курса валют
        total_base = json.loads(r.content)[keys[base]] * amount #обработка сконвертируемой суммы

        return total_base
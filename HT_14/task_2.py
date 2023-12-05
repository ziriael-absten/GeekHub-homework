# 2. Створіть програму для отримання курсу валют за певний період. 
# - отримати від користувача дату (це може бути як один день так і інтервал - початкова і 
# кінцева дати, продумайте механізм реалізації) і назву валюти
# - вивести курс по відношенню до гривні на момент вказаної дати (або за кожен день у вказаному 
# інтервалі)
# - не забудьте перевірку на валідність введених даних

import requests
from datetime import datetime, timedelta


class StatusCodeException(Exception):
    def __init__(self, value):
        self.value = value


def get_exchange_rate_on_date(date, currency_code):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise StatusCodeException(response.status_code)
        data = response.json()
        for rate in data['exchangeRate']:
            if rate['currency'] == currency_code:
                return rate['purchaseRateNB'], rate['saleRateNB']
        return None, None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None, None
    


def get_currency_exchange_rate_for_period(start_date, end_date, currency_code):
    current_date = start_date
    while current_date <= end_date:
        try:
            buy_rate, sale_rate = get_exchange_rate_on_date(current_date.strftime("%d.%m.%Y"), currency_code)
            if buy_rate is not None and sale_rate is not None:
                print(f"Currency {currency_code} for {current_date.strftime('%d.%m.%Y')}: Buy - {buy_rate}, Sale - {sale_rate}")
            else:
                print(f"There is no data for {currency_code} for {current_date.strftime('%d.%m.%Y')}")
            current_date += timedelta(days=1)
        except StatusCodeException as e:
            print(f"Unexpected status code: {e}")
            break


def start():
    try:
        currency_code = input("Enter currency code(for example: USD): ").upper()
        start_date_str = input("Enter date in format: 'dd.mm.yyyy': ")
        end_date_str = input("Enter end date in format 'dd.mm.yyyy' (can be empty): ")
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
        else:
            end_date = start_date
        if start_date > end_date:
            print("Date error")
        else:
            get_currency_exchange_rate_for_period(start_date, end_date, currency_code)
    except ValueError:
        print("Incorrect data")


start()

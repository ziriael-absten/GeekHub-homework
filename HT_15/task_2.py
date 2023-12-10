# 2. Викорисовуючи requests, заходите на ось цей сайт 
# "https://www.expireddomains.net/deleted-domains/" (з ним будьте обережні), вибираєте будь-яку 
# на ваш вибір доменну зону і парсите список  доменів - їх там буде десятки тисяч (звичайно 
# ураховуючи пагінацію). Всі отримані значення зберігти в CSV файл.

import csv
import time
import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(
            url=url,
            headers=headers,
        )
    return response.content


def write_to_csv(data):
    with open("domains.csv", "a", encoding="utf-8") as my_file:
        writer = csv.writer(my_file)
        for row in data:
            writer.writerow(row)


def start():
    result = []
    start_url = "https://www.expireddomains.net"
    url = "https://www.expireddomains.net/expired-domains/"
    while True:
        page = get_data(url)
        soup = BeautifulSoup(page, features="html.parser")
        listing_div = soup.find('div', {'id': 'listing'})
        if listing_div is None:
            print(f"Listing is not found on page {url}")
            break
        table = listing_div.find('table')
        if listing_div is None:
            print(f"Table is not found on page {url}")
            break
        td_elements = table.find_all('td', {'class': 'field_domain'})
        for td in td_elements:
            result.append(td.text)
        next_link = soup.find("a", "next")
        if next_link is None:
            print(f"Next link not found, finishing")
            break
        url = start_url + next_link['href']
        time.sleep(10)
    write_to_csv(result)


if __name__ == "__main__":
    start()

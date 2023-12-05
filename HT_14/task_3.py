# 3. http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної інформації про 
# записи: цитата, автор, інфа про автора тощо. 
# - збирається інформація з 10 сторінок сайту.
# - зберігати зібрані дані у CSV файл

import requests
from bs4 import BeautifulSoup
import csv


def scrape_quotes(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
                print(f"Unexpected status code: {response.status_code}")
                return None
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = []
        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            author_info_url = quote.find("a")["href"]
            author_info = scrape_author_info(f"http://quotes.toscrape.com{author_info_url}")
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            quotes.append({
                "text": text,
                "author": author,
                "author_info": author_info,
                "tags": ", ".join(tags)
            })
        return quotes
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def scrape_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    birth_date = soup.find("span", class_="author-born-date").text
    birth_place = soup.find("span", class_="author-born-location").text
    author_info = f'Birth Date: {birth_date}, Birth Place: {birth_place}'
    return author_info


def save_to_csv(quotes, filename="quotes.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["text", "author", "author_info", "tags"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quotes)


def start():
    all_quotes = []
    for page_number in range(1, 11):
        url = f"http://quotes.toscrape.com/page/{page_number}/"
        quotes = scrape_quotes(url)
        all_quotes.extend(quotes)
    save_to_csv(all_quotes)


start()

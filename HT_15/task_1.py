# 1. Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID категорії із сайту
# https://www.sears.com і буде збирати всі товари із цієї категорії, збирати по ним всі можливі
# дані (бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх у CSV файл (наприклад, якщо
# категорія має ID 12345, то файл буде називатись 12345_products.csv)
# Наприклад, категорія https://www.sears.com/tools-tool-storage/b-1025184 має ІД 1025184

import requests
from bs4 import BeautifulSoup
import csv
import time


class Product:
    def __init__(self, brand_name, name, category, price):
        self.brand_name = brand_name
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f"""
        Brand: {self.brand_name}
        Name: {self.name}
        Category: {self.category}
        Price: {self.price}"""


headers = {
    "Authorization": "SEARS",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


def write_to_csv(file_name, lst):
    with open(file_name, mode="a", newline="", encoding="utf-8") as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["Brand", "Name", "Category", "Price"])
        for product_instance in lst:
            writer.writerow(
                [
                    product_instance.brand_name,
                    product_instance.name,
                    product_instance.category,
                    product_instance.price,
                ]
            )


def start():
    category_id = input("Enter category id: ")
    url = "https://www.sears.com/api/sal/v3/products/search"
    file_name = f"{category_id}_products.csv"
    page_size = 48
    start_index = 1
    end_index = page_size
    wait = 2
    while True:
        lst = []
        params = {
            "startIndex": start_index,
            "endIndex": end_index,
            "searchType": "category",
            "store": "Sears",
            "storeId": 10153,
            "catGroupId": category_id,
        }
        time.sleep(wait)
        response = requests.get(url, headers=headers, params=params)
        print(response.status_code)
        print(f"Fetching {start_index}:{end_index}")
        if response.status_code == 429:
            wait = wait * 2
            print(f"Received too many requests... Waiting {wait} seconds")
            continue
        wait = 2
        if response.status_code != 200:
            print(
                f"Finished reading category {category_id}, total products: {len(lst)}"
            )
            break
        data = response.json()
        for i in data["items"]:
            name = i["name"]
            price = i["price"]["finalPrice"]
            category = i["category"]
            brand = i["brandName"]
            product_instance = Product(brand, name, category, price)
            lst.append(product_instance)
        start_index += page_size
        end_index += page_size
        time.sleep(2)
        write_to_csv(file_name, lst)


start()

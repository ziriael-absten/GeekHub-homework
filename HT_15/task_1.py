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
        self. price = price


    def __str__(self):
        return f"""
        Brand: {self.brand_name}
        Name: {self.name}
        Category: {self.category}
        Price: {self.price}"""


headers = {
    "Authorization":"SEARS",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

id_dict = {
    "1320301405" : "https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1320301405&seoURLPath=appliances-washers-dryers/1320301405",
    "1020022":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1020022&seoURLPath=appliances-refrigerators/1020022",
    "1020017":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1020017&seoURLPath=appliances-dishwashers/1020017",
    "1237483576":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1237483576&seoURLPath=appliances-bundles/1237483576",
    "1020019":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1020019&seoURLPath=appliances-freezers-ice-makers/1020019",
    "1025184":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1025184&seoURLPath=tools-tool-storage/1025184",
    "1020001":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=UNITS_HIGH_TO_LOW&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1020001&seoURLPath=lawn-garden/1020001",
    "1340929699":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1340931250&seoURLPath=fitness-sports-fitness-exercise-treadmills-accessories-treadmills/1340931250",
    "1231469010":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=1231469010&seoURLPath=tvs-electronics/1231469010",
    "5006935":"https://www.sears.com/api/sal/v3/products/search?searchType=category&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catGroupId=5006935&seoURLPath=clothing/5006935"
}


def write_to_csv(file_name, lst):
    with open(file_name, mode="w", newline="", encoding='utf-8') as my_file:
        writer = csv.writer(my_file)
        writer.writerow(["Brand", "Name", "Category", "Price"])
        for product_instance in lst:
            writer.writerow([product_instance.brand_name, product_instance.name, product_instance.category, product_instance.price])


def start():
    category_id = input("Enter category id: ")
    file_name = f"{category_id}_products.csv"
    url = id_dict[category_id]
    page_size = 48
    start_index = 1
    end_index = page_size
    lst = []
    wait = 2
    while True:
        params = {
            "startIndex":start_index,
            "endIndex":end_index
        }
        time.sleep(wait)
        response = requests.get(url, headers=headers, params=params)
        print(f"Fetching {start_index}:{end_index}")
        if response.status_code == 429:
            wait = wait * 2
            print(f"Received too many requests... Waiting {wait} seconds")
            continue
        wait = 2
        if response.status_code != 200:
            print(f"Finished reading category {category_id}, total products: {len(lst)}")
            break
        data = response.json()
        for i in data["items"]:
            name = (i["name"])
            price = (i["price"]["finalPrice"])
            category = (i["category"])
            brand = (i["brandName"])
            product_instance = Product(brand, name, category, price)
            lst.append(product_instance)
        start_index += page_size
        end_index += page_size
        time.sleep(2)
    write_to_csv(file_name, lst)


start()

# 3. Використовуючи Scrapy, заходите на "https://chrome.google.com/webstore/sitemap", переходите 
# на кожен лінк з тегів <loc>, з кожного лінка берете посилання на сторінки екстеншенів, парсите 
# їх і зберігаєте в CSV файл ID, назву та короткий опис кожного екстеншена (пошукайте уважно де 
# його можна взяти)

import scrapy


class GoogleExtensionSpider(scrapy.Spider):
    name = 'google_extension'
    start_urls = ['https://chrome.google.com/webstore/sitemap']

    def parse(self, response):
        # Extracting links from <loc> tags in the sitemap
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemaps = response.xpath('//ns:sitemap', namespaces=ns)
        for sitemap in sitemaps:
            loc = sitemap.xpath('./ns:loc/text()', namespaces=ns).get()
            yield scrapy.Request(url=loc, callback=self.parse_extensions_page)

    def parse_extensions_page(self, response):
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = response.xpath('//ns:url', namespaces=ns)
        for url in urls:
            loc = url.xpath('./ns:loc/text()', namespaces=ns).get()
            yield scrapy.Request(url=loc, callback=self.parse_extension_details)

    def parse_extension_details(self, response):
        strings = response.url.split('/')
        end = strings[-1]
        extension_id = end.split("?")[0]
        extension_name = response.css('meta[property="og:title"]::attr(content)').get()
        short_description = response.css('meta[property="og:description"]::attr(content)').get()
        print(f"extension_id: {extension_id}")
        print(f"extension_name: {extension_name}")
        print(f"short_description: {short_description}")
        if extension_id and extension_name and short_description:
            yield {
                'Extension ID': extension_id.strip(),
                'Extension Name': extension_name.strip(),
                'Short Description': short_description.strip(),
            }

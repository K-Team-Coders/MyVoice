import json
import time
import datetime
import os

import psycopg2
import scrapy
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path

from ..items import Object

load_dotenv(os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'DB.env'))

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DBNAME = os.getenv("DBNAME")


class AeromotusSpider(scrapy.Spider):
    name = "aeromotus"
    def start_requests(self):
        self.connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DBNAME
        )
        self.cursor = self.connection.cursor()
        urls = ['https://aeromotus.ru/shop/']

        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }

        for url in urls:
            yield scrapy.Request(url=url, method="POST", body="ppp=-1", headers=headers, callback=self.parse)

    def parse(self, response):
        cards = response.xpath('//div[@class="product-inner product-item__inner"]//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href')
        urls_ = []
        for card in cards:
            urls_.append(card.get())
        
        for url in urls_:
            yield scrapy.Request(url=url+"#tab-specification", method="GET", callback=self.parse_all_urls)

    def parse_all_urls(self, response):
        url_ = response.url
        name = response.xpath('//h1/text()').get()
        h3 = response.xpath('//div[@class="woocommerce-Tabs-panel woocommerce-Tabs-panel--specification panel entry-content wc-tab"]//h3/text()').getall()
            
        blocks_ = []
        tables = response.xpath('//table[@class="content_tbl"]')
        uls = response.xpath('//div[@class="woocommerce-Tabs-panel woocommerce-Tabs-panel--specification panel entry-content wc-tab"]//ul')
        if tables:
            for index_, table in enumerate(tables):
                th = table.xpath('.//tr//th/text()').getall()
                td = table.xpath('.//tr//td/text()').getall()
                data = ""
                for index, data_ in enumerate(th):
                    data = data + f"{th[index]} : {td[index]}"
                blocks_.append(h3[index_] + " : " + data )

        elif uls:
            for index_, ul in enumerate(uls):
                li = ul.xpath('.//li/text()').getall()
                blocks_.append(f"{h3[index_]} : {[li[index] for index, data in enumerate(li)]}")

        result = ""
        for block in blocks_:
            result = result + block

        # Запись
        if result:
            self.cursor.execute("INSERT INTO public.spiders VALUES (%s, %s, %s);", ('Aeromotus', str(url_), result))
            self.connection.commit()
        logger.debug('Sended data')

    def closed(self, reason):
        logger.error('Spider closed')
        self.connection.close()
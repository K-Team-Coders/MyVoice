import json
import datetime
import os
import random

import scrapy
import psycopg2
import requests
import pandas as pd
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from bs4 import BeautifulSoup as BS

from .languageModel.innterface import loadCosine, stats_method, cosine_sim, model_method

load_dotenv(os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'DB.env'))

SEARCH_QUERY = loadCosine()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DBNAME = os.getenv("DBNAME")

class MetaSpider(scrapy.Spider):
    name = "metaspider"
    
    def preprocessing_urls(self, urls):
        """
        Предобработка ссылок 
        """
        cleaned = []
        for url in urls:
            if len(url) > 0:

                # Нахождение ненужных юрлов по типу контакты, форумы и т.п.
                checker = False
                for item in self.rubbish:
                    if item in url:
                        checker = True      

                # Проверка на нахождение в том же домене (против бесконечных блужданий по интернету)
                domen_checker = False
                if self.current_domen in url:
                    domen_checker = True
                # Чек на вложенные запросы
                elif url[0] == '/':
                    domen_checker = False
                    checker = True
                    cleaned.append("https://" + str(self.current_domen) + str(url))

                # Финальный чек и проверка на PHP-производные сайты
                if not checker and domen_checker:
                    cleaned.append(url)
        
        return cleaned

    def start_requests(self):
        self.connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DBNAME
        )
        self.rubbish = ["policy", "instagram", "wp-content", "terms", "webinar", "footer", "download", "service", "youtube", "login", "pdf", "jpeg", "img", "jpg", "png", "sign", "support", "logout","faq", "blog", "develop","javascript", "accounts", "auth", "user", "forum", "contacts", "facebook", "#page", "cart", "tel", "@", "company", "personal", "action"]
        self.cursor = self.connection.cursor()
        self.current_domen = ''

        self.visited = []
        self.sitemap = []

        self.headers = []

        self.dataframe = pd.DataFrame(columns=['source', 'url', 'extracted'])

        with open(os.path.join(Path.cwd().joinpath('collecter').joinpath('spiders'), 'agents.json')) as f:
            self.headers = json.load(f)
        
        urls = [
            # 'https://aeromotus.ru/product/dji-matrice-30t/',
            # 'https://aeromotus.ru/webinar/dji-mavic-3-seriya-enterprise/',
            # 'https://aeromotus.ru/', 
            # "https://nelk.ru/", 
            "https://dji.com/", 
            "https://geobox.ru/"
        ]

        for url in urls:
            left = url.find('//') + 2
            right = url[left:].find('/') + left
            self.current_domen = url[left:right]
            yield scrapy.Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        filtered = False
        logger.debug(response.url)

        for item in self.rubbish:
            if item in response.url:
                logger.debug('Filter error')
                filtered = True

        # Добаляем в посещенные (статистика)
        self.visited.append(response.url)
        # Если произоша ошибка фильтрации - пропускаем обработку (смысла не имеет)
        if not filtered:
            try:
                # Добавление юрлов
                body = response.xpath('//div')
                urls = body.css('a::attr(href)').extract()
                cleaned = self.preprocessing_urls(urls)
                self.sitemap.extend(cleaned)
                self.sitemap = list(set(self.sitemap))

                # Обработка текста
                soup = BS(response.text, 'html.parser')
                # # Нашли слово характеристики
                params = soup.find(text='Характеристики')
                if params:
                    # Если нашли в ссылке - продолжаем парсинг
                    try:
                        href = params.parent.get('href')
                        header = {
                            "User-Agent": self.headers[random.randrange(0, len(self.headers))]["user_agent"]
                        }
                        # Если кнопка
                        if href[0] == '/':
                            link = response.url + href
                            logger.success(f"Кнопка-ссылка {link}")
                            self.process(link, header)
                        # Если PHP - стиль
                        elif href[0] == '#':
                            link = response.url + href
                            logger.success(f"PHP ссылка {link}")
                            self.process(link, header)

                        # Если стандартный переход 
                        else:
                            logger.success(f"Нормальная ссылка {href}")
                            self.process(href, header)

                    except Exception as e:
                        logger.error(e)
                    except:
                        logger.error('Not a href inside!')

                # Не нашли характеристики? https://i.pinimg.com/originals/01/e6/c2/01e6c2368a9720c63ac7a981c4500302.png
                # Ищем дальше по тому что есть 
                # Рано или поздно натыкаемся на юрл с характеристиками
                for url in cleaned:
                    if url not in self.visited:
                        header = {
                            "User-Agent": self.headers[random.randrange(0, len(self.headers))]["user_agent"]
                        }
                        yield scrapy.Request(url=url, method="GET", headers=header, callback=self.parse)
            except Exception as e:
                logger.error(e)
        
    def process(self, url, header):
        """
        Функция обработки OL, UL, TABLE
        """
        logger.debug(f'Processing {url}')
        response = requests.get(url, headers=header)
        html = BS(response.text, 'html.parser')
        total_information = []
        
        # Находим на странице информационные ресурсы
        tables = html.find_all('table')
        uls = html.find_all('ul')
        ols = html.find_all('ol')
        h = html.find_all('h')

        # Добавляем в единый список
        total_information.extend(tables)
        total_information.extend(uls)
        total_information.extend(ols)
        total_information.extend(h)

        # Проверка
        for item in total_information:

            # ИСПОЛЬЗОВАТЬ ЛИБО БЛИЗОСТЬ ПО КОСИНУСУ, ЛИБО ПО СРЕДНЕАРИФМЕТИЧЕСКОМУ ОБЩЕЙ БЛИЗОСТИ СЛОВ !!!
            # В исходниках функций подробнее

            # param = stats_method(SEARCH_QUERY, item.text)
            param = cosine_sim(SEARCH_QUERY, item.text)
            # param = model_method(SEARCH_QUERY, item.text)
            if param > 0.01:               
                seria = pd.Series(index=['source', 'url', 'extracted'], data=[self.current_domen, url, item.text])
                self.dataframe = self.dataframe.append(seria, ignore_index=True)
                
                text = ''
                if len(item.text) > 500:
                    text = item.text[:499]
                else:
                    text = item.text

                # Проверка 
                self.cursor.execute("SELECT * FROM spiders WHERE spider=%s AND url=%s AND data=%s", ('MetaSpider', url, text))
                if self.cursor.fetchall():
                   pass
                else: 
                # Добавление в БДx
                    self.cursor.execute("INSERT INTO spiders VALUES (%s, %s, %s);", ('MetaSpider', url, text))
                    self.connection.commit()
        
        # Запись в XLSX
        self.dataframe.to_excel('result.xlsx', engine='xlsxwriter')
        

    def closed(self, reason):
        logger.debug(reason)
        logger.success(f"Crawled {len(self.visited)}")
        logger.success(f"Total {len(self.sitemap)}")
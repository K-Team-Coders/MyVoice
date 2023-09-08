from pathlib import Path
import scrapy

import json
import os
from loguru import logger
import psycopg2

from dotenv import load_dotenv
load_dotenv(os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'DB.env'))

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DBNAME = os.getenv("DBNAME")

class DronesCnasSpider(scrapy.Spider):
    name = "dronescnas"

    def start_requests(self):
        self.connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DBNAME
        )
        self.cursor = self.connection.cursor()

        urls = [
            'https://drones.cnas.org/drones/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cards = response.xpath('//div[@class="drone-box"]')
        for card in cards:
            drone_name = card.xpath('.//div[@class="drone-name has-thumbnail"]//h2/text()').get()
            if drone_name == None:
                drone_name = 'Unnamed'

            drone_picture = card.xpath('.//div[@class="drone-name has-thumbnail"]').attrib['style']
            drone_picture = drone_picture[drone_picture.find('(')+2:len(drone_picture)-3]

            logger.debug(drone_picture)
            data = card.xpath('.//dd/text()').getall()

            jsoned = json.dumps({
                'picture': drone_picture,
                'company': data[1],
                'platform': data[2],
                'endurance': data[3],
                "payload": data[5].split()[0],
                "max_speed": data[6].split()[0],
                "altitude": data[7].split()[0],
                "mass": data[8].split()[0],
                "width": data[9].split()[0],
                "length": data[10].split()[0],
                })

            
            logger.debug(jsoned)
            country = data[0]
            range_ =  data[4]
            if "-" in range_:
                range_ = 0.0
            else:
                range_ = range_.split()[0]
            try:
                self.cursor.execute('INSERT INTO public.dronescnas VALUES (%s, %s, %s, %s);', (drone_name, country, range_, jsoned))
                self.connection.commit()
            except Exception as e:
                logger.error(e)